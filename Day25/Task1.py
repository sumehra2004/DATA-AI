# ============================
# End-to-end ML workflow in ONE script
# Dataset: UCI Adult (real-world) via OpenML
# Tasks covered:
# - Load + explore dataset (head, shape, dtypes, numeric/cat columns)
# - Visualize distributions (2 numeric features)
# - Train/test split
# - Missing value handling (SimpleImputer)
# - Scaling (StandardScaler)
# - Encoding (OneHotEncoder)
# - ColumnTransformer preprocessing
# - Pipelines: basic, full preprocessing, SelectKBest, PolynomialFeatures, PCA
# - Evaluation: accuracy, confusion matrix, cross-val, learning curve
# - Hyperparameter tuning: GridSearchCV, RandomizedSearchCV (C, n_estimators, max_depth)
# - Advanced: custom transformer, FunctionTransformer, FeatureUnion, nested pipeline
# - Interpretation: feature importance (tree), PDP, SHAP-style conceptual contributions
# - Residual analysis (probability residuals)
# ============================

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV, learning_curve
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PolynomialFeatures, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import PartialDependenceDisplay

from sklearn.base import BaseEstimator, TransformerMixin
from scipy import sparse
from scipy.stats import randint, loguniform


# ----------------------------
# 1) Data Loading and Exploration
# ----------------------------
adult = fetch_openml(name="adult", version=2, as_frame=True)
df = adult.frame.copy()

# target column in Adult dataset is commonly named "class"
target_col = "class"
if target_col not in df.columns:
    # fallback if OpenML uses a different name (rare)
    target_col = df.columns[-1]

# Replace '?' with NaN (Adult dataset uses '?' for missing in some categorical columns)
df = df.replace("?", np.nan)

print("\n===== FIRST 10 ROWS =====")
print(df.head(10))

print("\n===== DATASET INFO =====")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print("\nDtypes:")
print(df.dtypes)

X = df.drop(columns=[target_col])
y = df[target_col]

num_cols = X.select_dtypes(include=["number", "bool"]).columns.tolist()
cat_cols = [c for c in X.columns if c not in num_cols]

print("\n===== FEATURE TYPES =====")
print(f"Numerical columns ({len(num_cols)}): {num_cols}")
print(f"Categorical columns ({len(cat_cols)}): {cat_cols}")

# Visualize distributions of at least two numerical features (if available)
numeric_for_plots = [c for c in ["age", "hours-per-week", "education-num", "capital-gain", "capital-loss"] if c in num_cols]
if len(numeric_for_plots) < 2 and len(num_cols) >= 2:
    numeric_for_plots = num_cols[:2]

if len(numeric_for_plots) >= 2:
    plt.figure()
    plt.hist(X[numeric_for_plots[0]].dropna(), bins=30)
    plt.title(f"Distribution: {numeric_for_plots[0]}")
    plt.xlabel(numeric_for_plots[0])
    plt.ylabel("Count")
    plt.show()

    plt.figure()
    plt.hist(X[numeric_for_plots[1]].dropna(), bins=30)
    plt.title(f"Distribution: {numeric_for_plots[1]}")
    plt.xlabel(numeric_for_plots[1])
    plt.ylabel("Count")
    plt.show()
else:
    print("\n[Note] Not enough numeric columns found to plot 2 distributions.")


# ----------------------------
# 2) Data Preprocessing (Split, Impute, Scale, Encode, ColumnTransformer)
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

numeric_preprocess = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_preprocess = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    # min_frequency reduces huge one-hot explosion; good for PCA later
    ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=10)),
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_preprocess, num_cols),
        ("cat", categorical_preprocess, cat_cols),
    ],
    remainder="drop",
)


# ----------------------------
# 3) Building Machine Learning Pipelines
# ----------------------------

# (A) Basic pipeline: StandardScaler + LogisticRegression
# This is meaningful for numeric-only features.
basic_numeric_only = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=2000))
])

if len(num_cols) > 0:
    basic_numeric_only.fit(X_train[num_cols], y_train)
    y_pred_basic = basic_numeric_only.predict(X_test[num_cols])
    print("\n===== BASIC PIPELINE (NUMERIC ONLY): StandardScaler + LogisticRegression =====")
    print("Accuracy:", accuracy_score(y_test, y_pred_basic))
else:
    print("\n[Note] No numeric columns found for the basic scaler+logreg demo.")

# (B) Pipeline with preprocessing (ColumnTransformer) + LogisticRegression
clf_logreg = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("logreg", LogisticRegression(max_iter=2000))
])

# (C) Pipeline with feature selection SelectKBest
clf_kbest = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("selectk", SelectKBest(score_func=mutual_info_classif, k=50)),
    ("logreg", LogisticRegression(max_iter=2000))
])

# (D) Pipeline with PolynomialFeatures (for numeric features) inside numeric preprocessing
numeric_poly_preprocess = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler()),
])

preprocessor_poly = ColumnTransformer(
    transformers=[
        ("num", numeric_poly_preprocess, num_cols),
        ("cat", categorical_preprocess, cat_cols),
    ],
    remainder="drop",
)

clf_poly = Pipeline(steps=[
    ("preprocess", preprocessor_poly),
    ("logreg", LogisticRegression(max_iter=2000))
])

# (E) Pipeline with PCA (convert sparse -> dense first, then PCA)
def to_dense(Xm):
    return Xm.toarray() if sparse.issparse(Xm) else Xm

clf_pca = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("to_dense", FunctionTransformer(to_dense, accept_sparse=True)),
    ("pca", PCA(n_components=30, random_state=42)),
    ("logreg", LogisticRegression(max_iter=2000))
])


# ----------------------------
# 4) Model Evaluation (accuracy, confusion matrix, CV, learning curve)
# ----------------------------
print("\n===== TRAIN + EVALUATE (Preprocess + LogisticRegression) =====")
clf_logreg.fit(X_train, y_train)
y_pred = clf_logreg.predict(X_test)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=clf_logreg.classes_)

print("Accuracy:", acc)
print("Confusion Matrix (rows=true, cols=pred):")
print("Labels:", clf_logreg.classes_)
print(cm)

print("\n===== CROSS-VALIDATION (5-fold) =====")
cv_scores = cross_val_score(clf_logreg, X, y, cv=5, scoring="accuracy")
print("CV Accuracy scores:", np.round(cv_scores, 4))
print("CV Mean Accuracy:", float(np.mean(cv_scores)))

print("\n===== COMPARE: Train-Test vs Cross-Val =====")
print("Train-Test Accuracy:", float(acc))
print("CV Mean Accuracy:", float(np.mean(cv_scores)))

# Learning curve
print("\n===== LEARNING CURVE =====")
train_sizes, train_scores, val_scores = learning_curve(
    clf_logreg, X, y, cv=5, scoring="accuracy",
    train_sizes=np.linspace(0.1, 1.0, 8),
    n_jobs=-1,
    random_state=42
)

plt.figure()
plt.plot(train_sizes, train_scores.mean(axis=1), marker="o", label="Train")
plt.plot(train_sizes, val_scores.mean(axis=1), marker="o", label="CV")
plt.title("Learning Curve (Preprocess + LogisticRegression)")
plt.xlabel("Training examples")
plt.ylabel("Accuracy")
plt.legend()
plt.show()


# ----------------------------
# 5) Hyperparameter Tuning (GridSearchCV + RandomizedSearchCV)
# Includes examples: regularization parameter (C), number of estimators, max depth
# ----------------------------

# (A) GridSearchCV for LogisticRegression (regularization parameter)
grid_logreg = GridSearchCV(
    estimator=clf_logreg,
    param_grid={
        "logreg__C": [0.01, 0.1, 1, 10],
        "logreg__penalty": ["l2"],
        "logreg__solver": ["lbfgs"]
    },
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)
grid_logreg.fit(X_train, y_train)
print("\n===== GRID SEARCH (LogisticRegression) =====")
print("Best params:", grid_logreg.best_params_)
print("Best CV score:", float(grid_logreg.best_score_))
print("Test accuracy of best model:", float(accuracy_score(y_test, grid_logreg.best_estimator_.predict(X_test))))

# (B) RandomForest pipeline + Grid/Random search for n_estimators and max_depth
rf_pipe = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("rf", RandomForestClassifier(random_state=42, n_jobs=-1))
])

grid_rf = GridSearchCV(
    estimator=rf_pipe,
    param_grid={
        "rf__n_estimators": [100, 300],
        "rf__max_depth": [None, 10, 20],
        "rf__min_samples_split": [2, 10],
    },
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)
grid_rf.fit(X_train, y_train)

rand_rf = RandomizedSearchCV(
    estimator=rf_pipe,
    param_distributions={
        "rf__n_estimators": randint(80, 500),
        "rf__max_depth": [None, 5, 10, 15, 20, 30],
        "rf__min_samples_split": randint(2, 20),
        "rf__max_features": ["sqrt", "log2", None],
    },
    n_iter=25,
    cv=5,
    scoring="accuracy",
    random_state=42,
    n_jobs=-1
)
rand_rf.fit(X_train, y_train)

print("\n===== GRID SEARCH (RandomForest) =====")
print("Best params:", grid_rf.best_params_)
print("Best CV score:", float(grid_rf.best_score_))
print("Test accuracy:", float(accuracy_score(y_test, grid_rf.best_estimator_.predict(X_test))))

print("\n===== RANDOMIZED SEARCH (RandomForest) =====")
print("Best params:", rand_rf.best_params_)
print("Best CV score:", float(rand_rf.best_score_))
print("Test accuracy:", float(accuracy_score(y_test, rand_rf.best_estimator_.predict(X_test))))

print("\n===== COMPARE: GridSearchCV vs RandomizedSearchCV (RandomForest) =====")
print("Grid best CV:", float(grid_rf.best_score_), "| Test:", float(accuracy_score(y_test, grid_rf.best_estimator_.predict(X_test))))
print("Rand best CV:", float(rand_rf.best_score_), "| Test:", float(accuracy_score(y_test, rand_rf.best_estimator_.predict(X_test))))


# ----------------------------
# 6) Advanced Pipeline Techniques
# ----------------------------

# (A) Custom transformer using BaseEstimator + TransformerMixin
# Example: add a new numeric feature: log1p(capital-gain) if it exists
class AddLogCapitalGain(BaseEstimator, TransformerMixin):
    def __init__(self, col_name="capital-gain"):
        self.col_name = col_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        Xc = X.copy()
        if self.col_name in Xc.columns:
            Xc[self.col_name + "_log1p"] = np.log1p(pd.to_numeric(Xc[self.col_name], errors="coerce"))
        return Xc

# (B) FunctionTransformer for a custom function to a feature
# Example: clip hours-per-week to a max (if exists)
def clip_hours(df_in):
    df_out = df_in.copy()
    col = "hours-per-week"
    if col in df_out.columns:
        df_out[col] = pd.to_numeric(df_out[col], errors="coerce").clip(upper=80)
    return df_out

advanced_pre = Pipeline(steps=[
    ("add_log_gain", AddLogCapitalGain("capital-gain")),
    ("clip_hours", FunctionTransformer(clip_hours, feature_names_out="one-to-one")),
])

# Recompute columns after advanced feature engineering (so new column is included if created)
X_adv = advanced_pre.fit_transform(X)
num_cols_adv = X_adv.select_dtypes(include=["number", "bool"]).columns.tolist()
cat_cols_adv = [c for c in X_adv.columns if c not in num_cols_adv]

preprocessor_adv = ColumnTransformer(
    transformers=[
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), num_cols_adv),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=10))]), cat_cols_adv),
    ],
    remainder="drop",
)

# (C) FeatureUnion to combine multiple feature extraction pipelines (numeric only example)
# We'll select numeric columns and build two parallel transforms:
numeric_selector = ColumnTransformer(
    transformers=[("num_only", "passthrough", num_cols_adv)],
    remainder="drop"
)

numeric_scaled = Pipeline(steps=[
    ("num_sel", numeric_selector),
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

numeric_poly = Pipeline(steps=[
    ("num_sel", numeric_selector),
    ("imputer", SimpleImputer(strategy="median")),
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler())
])

union_features = FeatureUnion([
    ("scaled", numeric_scaled),
    ("poly", numeric_poly),
])

# (D) Nested pipeline combining preprocessing and model training
nested_pipeline = Pipeline(steps=[
    ("advanced_fe", advanced_pre),
    ("preprocess", preprocessor_adv),
    ("selectk", SelectKBest(score_func=mutual_info_classif, k=60)),
    ("logreg", LogisticRegression(max_iter=2000))
])

X_train_adv, X_test_adv, y_train_adv, y_test_adv = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

nested_pipeline.fit(X_train_adv, y_train_adv)
nested_pred = nested_pipeline.predict(X_test_adv)
print("\n===== ADVANCED NESTED PIPELINE (CustomTransformer + FunctionTransformer + Preprocess + SelectKBest + LogReg) =====")
print("Accuracy:", float(accuracy_score(y_test_adv, nested_pred)))


# ----------------------------
# 7) Model Interpretation
# ----------------------------

# (A) Feature importance using a tree-based model (RandomForest)
best_rf = rand_rf.best_estimator_  # use tuned RF

# Get feature names after preprocessing
ohe = best_rf.named_steps["preprocess"].named_transformers_["cat"].named_steps["onehot"]
cat_feature_names = ohe.get_feature_names_out(cat_cols)
feature_names = np.array(num_cols + list(cat_feature_names))

importances = best_rf.named_steps["rf"].feature_importances_
top_idx = np.argsort(importances)[-20:][::-1]

plt.figure()
plt.barh(feature_names[top_idx][::-1], importances[top_idx][::-1])
plt.title("Top 20 Feature Importances (RandomForest)")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.show()

# (B) Partial Dependence Plot for one feature (use 'age' if present; else first numeric)
pdp_feature = "age" if "age" in X.columns else (num_cols[0] if len(num_cols) else None)
if pdp_feature is not None:
    plt.figure()
    PartialDependenceDisplay.from_estimator(
        best_rf, X_test, [pdp_feature], kind="average", grid_resolution=30
    )
    plt.show()
else:
    print("\n[Note] No numeric feature available for PDP.")

# (C) Conceptual SHAP-style plot: per-feature contributions for Logistic Regression on ONE test row
# We'll use the tuned logistic regression model from GridSearch (best_estimator_)
best_lr = grid_logreg.best_estimator_
# prepare a single row
x1 = X_test.iloc[[0]]
# transform to feature space
X1_trans = best_lr.named_steps["preprocess"].transform(x1)
# get names
ohe_lr = best_lr.named_steps["preprocess"].named_transformers_["cat"].named_steps["onehot"]
feature_names_lr = np.array(num_cols + list(ohe_lr.get_feature_names_out(cat_cols)))

# LogisticRegression contributions: coef * feature_value (for the positive class decision)
lr_model = best_lr.named_steps["logreg"]
coef = lr_model.coef_.ravel()

# sparse-safe multiply
if sparse.issparse(X1_trans):
    xvec = X1_trans.toarray().ravel()
else:
    xvec = np.asarray(X1_trans).ravel()

contrib = coef * xvec
top = 15
top_c_idx = np.argsort(np.abs(contrib))[-top:][::-1]

plt.figure()
plt.barh(feature_names_lr[top_c_idx][::-1], contrib[top_c_idx][::-1])
plt.title("Conceptual SHAP-style Contributions (LogReg, 1 sample)")
plt.xlabel("Contribution (coef * value)")
plt.ylabel("Feature")
plt.show()

# (D) Residual analysis: predicted probability vs residuals (residual = y_true - p(positive))
# pick a "positive" class label for probability column
pos_label = best_lr.named_steps["logreg"].classes_[1]  # assumes binary classification

proba = best_lr.predict_proba(X_test)[:, 1]
y_true01 = (y_test == pos_label).astype(int).to_numpy()
residuals = y_true01 - proba

plt.figure()
plt.scatter(proba, residuals, s=10)
plt.title("Residual Analysis (Classification): Predicted Prob vs Residual (y - p)")
plt.xlabel(f"Predicted P({pos_label})")
plt.ylabel("Residual")
plt.axhline(0)
plt.show()


# ----------------------------
# Extra: run the other pipelines quickly (kbest, poly, pca)
# ----------------------------
print("\n===== QUICK CHECK: Other Pipelines =====")
for name, model in [
    ("SelectKBest + LogReg", clf_kbest),
    ("PolynomialFeatures + LogReg", clf_poly),
    ("PCA + LogReg", clf_pca),
]:
    try:
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        print(f"{name:30s} | Accuracy: {accuracy_score(y_test, pred):.4f}")
    except Exception as e:
        print(f"{name:30s} | Skipped (error): {e}")