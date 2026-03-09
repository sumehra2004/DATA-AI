# ===============================
# 1. Import Libraries
# ===============================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV, learning_curve, validation_curve
from sklearn.preprocessing import StandardScaler, MinMaxScaler, PolynomialFeatures, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.inspection import PartialDependenceDisplay

# ===============================
# 2. Load Dataset
# ===============================
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
df["Target"] = data.target

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print(df.dtypes)

# ===============================
# 3. Identify Features
# ===============================
num_features = df.select_dtypes(include=['float64','int64']).columns.tolist()
num_features.remove("Target")

print("Numerical Features:", num_features)

# ===============================
# 4. Missing Values
# ===============================
print("Missing Values:\n", df.isnull().sum())

# ===============================
# 5. Visualization
# ===============================
plt.figure()
sns.histplot(df["MedInc"], kde=True)
plt.title("Income Distribution")

plt.figure()
sns.heatmap(df.corr(), annot=True)
plt.title("Correlation Matrix")

plt.figure()
plt.scatter(df["MedInc"], df["HouseAge"])
plt.xlabel("MedInc")
plt.ylabel("HouseAge")

# ===============================
# 6. Train Test Split
# ===============================
X = df.drop("Target", axis=1)
y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 7. Preprocessing
# ===============================
imputer = SimpleImputer(strategy="median")

scaler_standard = StandardScaler()
scaler_minmax = MinMaxScaler()

preprocessor = Pipeline([
    ("imputer", imputer),
    ("scaler", scaler_standard)
])

# visualize scaling effect
scaled_data = scaler_standard.fit_transform(X)
plt.figure()
sns.histplot(scaled_data[:,0], kde=True)
plt.title("Scaled Feature Distribution")

# ===============================
# 8. Basic Pipeline (Linear Regression)
# ===============================
pipe_lr = Pipeline([
    ("preprocess", preprocessor),
    ("model", LinearRegression())
])

pipe_lr.fit(X_train, y_train)
pred_lr = pipe_lr.predict(X_test)

print("Linear Regression R2:", r2_score(y_test, pred_lr))

# ===============================
# 9. RandomForest Pipeline
# ===============================
pipe_rf = Pipeline([
    ("preprocess", preprocessor),
    ("model", RandomForestRegressor())
])

pipe_rf.fit(X_train, y_train)
pred_rf = pipe_rf.predict(X_test)

print("RandomForest R2:", r2_score(y_test, pred_rf))

# ===============================
# 10. Polynomial Features
# ===============================
pipe_poly = Pipeline([
    ("preprocess", preprocessor),
    ("poly", PolynomialFeatures(degree=2)),
    ("model", LinearRegression())
])

# ===============================
# 11. Feature Selection
# ===============================
pipe_select = Pipeline([
    ("preprocess", preprocessor),
    ("select", SelectKBest(score_func=f_regression, k=5)),
    ("model", LinearRegression())
])

# ===============================
# 12. PCA Pipeline
# ===============================
pipe_pca = Pipeline([
    ("preprocess", preprocessor),
    ("pca", PCA(n_components=5)),
    ("model", LinearRegression())
])

pipe_pca.fit(X_train, y_train)
pred_pca = pipe_pca.predict(X_test)

print("R2 with PCA:", r2_score(y_test, pred_pca))

# ===============================
# 13. Cross Validation
# ===============================
scores = cross_val_score(pipe_rf, X, y, cv=5)
print("Cross Validation Scores:", scores)

# ===============================
# 14. Learning Curve
# ===============================
train_sizes, train_scores, test_scores = learning_curve(
    pipe_rf, X, y, cv=5
)

plt.figure()
plt.plot(train_sizes, train_scores.mean(axis=1), label="Train")
plt.plot(train_sizes, test_scores.mean(axis=1), label="Validation")
plt.legend()

# ===============================
# 15. Validation Curve
# ===============================
param_range = [10,50,100]

train_scores, test_scores = validation_curve(
    RandomForestRegressor(),
    X,
    y,
    param_name="n_estimators",
    param_range=param_range,
    cv=3
)

plt.figure()
plt.plot(param_range, test_scores.mean(axis=1))

# ===============================
# 16. Hyperparameter Tuning
# ===============================
param_grid = {
    "model__n_estimators":[50,100],
    "model__max_depth":[5,10,None]
}

grid = GridSearchCV(pipe_rf, param_grid, cv=3)
grid.fit(X_train, y_train)

print("Best Parameters:", grid.best_params_)

param_dist = {
    "model__n_estimators":[50,100,200],
    "model__max_depth":[None,5,10,20]
}

random = RandomizedSearchCV(pipe_rf, param_dist, n_iter=5, cv=3)
random.fit(X_train, y_train)

print("Random Search Best:", random.best_params_)

# ===============================
# 17. Custom Transformer
# ===============================
class CustomFeature(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = pd.DataFrame(X)
        X["Income_Age"] = X.iloc[:,0] * X.iloc[:,1]
        return X

# ===============================
# 18. FunctionTransformer
# ===============================
log_transform = FunctionTransformer(np.log1p)

# ===============================
# 19. FeatureUnion
# ===============================
union = FeatureUnion([
    ("pca", PCA(n_components=3)),
    ("select", SelectKBest(f_regression, k=3))
])

# ===============================
# 20. Nested Pipeline
# ===============================
nested_pipe = Pipeline([
    ("custom", CustomFeature()),
    ("preprocess", preprocessor),
    ("features", union),
    ("model", RandomForestRegressor())
])

nested_pipe.fit(X_train, y_train)

# ===============================
# 21. Feature Importance
# ===============================
rf = RandomForestRegressor()
rf.fit(X_train, y_train)

importances = rf.feature_importances_

plt.figure()
plt.bar(X.columns, importances)
plt.xticks(rotation=90)
plt.title("Feature Importance")

# ===============================
# 22. Partial Dependence Plot
# ===============================
PartialDependenceDisplay.from_estimator(
    rf,
    X_test,
    [0]
)

# ===============================
# 23. Residual Analysis
# ===============================
pred = rf.predict(X_test)
residuals = y_test - pred

plt.figure()
plt.scatter(pred, residuals)
plt.axhline(0)
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.title("Residual Plot")

plt.show()

# ===============================
# 24. Final Model Summary
# ===============================
print("Final Model R2:", r2_score(y_test, pred))
print("Key Features:", list(X.columns))
print("Insight: Income and house age strongly influence house price.")