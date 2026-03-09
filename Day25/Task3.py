# =======================
# Import Libraries
# =======================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV, learning_curve, validation_curve
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder, PolynomialFeatures, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_regression, VarianceThreshold
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.inspection import PartialDependenceDisplay

# =======================
# Data Collection & Loading
# =======================
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
df["Target"] = data.target

print(df.head(10))
print("Shape:", df.shape)
print(df.dtypes)
print("Duplicates:", df.duplicated().sum())

# =======================
# Exploratory Data Analysis
# =======================
print("Missing values:\n", df.isnull().sum())

plt.figure(); sns.histplot(df["MedInc"], kde=True)
plt.figure(); df[["MedInc","HouseAge"]].hist()

plt.figure(); sns.boxplot(x=df["MedInc"])

plt.figure(); plt.scatter(df["MedInc"], df["Target"])
plt.xlabel("Income"); plt.ylabel("House Value")

corr = df.corr()
plt.figure(); sns.heatmap(corr, annot=True)

print("Most correlated with Target:\n", corr["Target"].sort_values(ascending=False))

# =======================
# Data Preprocessing
# =======================
X = df.drop("Target", axis=1)
y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

num_features = X.columns

num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_features)
])

X_train_p = preprocessor.fit_transform(X_train)
X_test_p = preprocessor.transform(X_test)

# =======================
# Feature Engineering
# =======================
poly = PolynomialFeatures(2)
X_poly = poly.fit_transform(X_train_p)

selector = SelectKBest(score_func=f_regression, k=5)
X_selected = selector.fit_transform(X_poly, y_train)

var_filter = VarianceThreshold(0.1)
X_var = var_filter.fit_transform(X_selected)

pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_var)

plt.figure()
plt.scatter(X_pca[:,0], X_pca[:,1])

print("Before PCA:", X_train.shape)
print("After PCA:", X_pca.shape)

# =======================
# Model Building
# =======================
models = {
"LinearRegression": LinearRegression(),
"DecisionTree": DecisionTreeRegressor(),
"RandomForest": RandomForestRegressor(),
"SVM": SVR()
}

for name,model in models.items():
    model.fit(X_train_p,y_train)
    pred = model.predict(X_test_p)
    print(name,"R2:",r2_score(y_test,pred))

# =======================
# Pipeline Model
# =======================
pipe = Pipeline([
("preprocess",preprocessor),
("model",RandomForestRegressor())
])

pipe.fit(X_train,y_train)
pred_pipe = pipe.predict(X_test)
print("Pipeline R2:", r2_score(y_test,pred_pipe))

# =======================
# Model Evaluation
# =======================
cv_scores = cross_val_score(pipe,X,y,cv=5)
print("Cross Validation:",cv_scores)

train_sizes,train_scores,test_scores = learning_curve(pipe,X,y,cv=5)

plt.figure()
plt.plot(train_sizes,train_scores.mean(axis=1))
plt.plot(train_sizes,test_scores.mean(axis=1))

param_range=[10,50,100]
train_scores,test_scores = validation_curve(
RandomForestRegressor(),X,y,param_name="n_estimators",param_range=param_range,cv=3)

plt.figure()
plt.plot(param_range,test_scores.mean(axis=1))

# =======================
# Hyperparameter Tuning
# =======================
param_grid={"model__n_estimators":[50,100],
            "model__max_depth":[5,10,None]}

grid = GridSearchCV(pipe,param_grid,cv=3)
grid.fit(X_train,y_train)
print("Best Grid Params:",grid.best_params_)

param_dist={"model__n_estimators":[50,100,200],
            "model__max_depth":[None,5,10,20]}

random = RandomizedSearchCV(pipe,param_dist,n_iter=5,cv=3)
random.fit(X_train,y_train)
print("Best Random Params:",random.best_params_)

# =======================
# Advanced Pipelines
# =======================
class CustomFeature(BaseEstimator,TransformerMixin):
    def fit(self,X,y=None): return self
    def transform(self,X):
        X=pd.DataFrame(X)
        X["Income_Age"]=X.iloc[:,0]*X.iloc[:,1]
        return X

log_transform = FunctionTransformer(np.log1p)

union = FeatureUnion([
("pca",PCA(n_components=2)),
("select",SelectKBest(f_regression,k=2))
])

nested = Pipeline([
("custom",CustomFeature()),
("preprocess",preprocessor),
("features",union),
("model",RandomForestRegressor())
])

nested.fit(X_train,y_train)

# =======================
# Model Interpretation
# =======================
rf = RandomForestRegressor()
rf.fit(X_train,y_train)

importance = rf.feature_importances_

plt.figure()
plt.bar(X.columns,importance)
plt.xticks(rotation=90)

PartialDependenceDisplay.from_estimator(rf,X_test,[0])

pred = rf.predict(X_test)
residuals = y_test - pred

plt.figure()
plt.scatter(pred,residuals)
plt.axhline(0)

plt.show()