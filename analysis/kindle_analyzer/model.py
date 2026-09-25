"""Which listing traits go with Amazon's Best Seller badge?

The badge is rare (about 1.7% of listings), so accuracy is meaningless here:
always answering "not a bestseller" is ~98% accurate. Models are judged on
ranking quality instead (PR-AUC, ROC-AUC, precision in the top 1%), always
next to a no-skill baseline.

Listings of the same book (editions, categories) are kept on one side of every
split with StratifiedGroupKFold, so the model cannot score well by recognising
a book it already saw in training.

Note on meaning: star ratings and review counts are measured at the same time
as the badge, so this describes association, not a forecast of future sales.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEED = 42
NUMERIC = ["log_price", "stars", "log_reviews", "pub_year"]
BINARY = ["is_free", "is_ku", "reviews_recorded", "has_pub_date"]
# Editors' Pick and Goodreads Choice are left out on purpose: a listing shows at
# most one badge, so those flags would tell the model "this is not a bestseller".
CATEGORICAL = ["category", "publisher_group"]
FEATURES = NUMERIC + BINARY + CATEGORICAL

LABELS = {
    "log_price": "Price",
    "stars": "Star rating",
    "log_reviews": "Review count",
    "pub_year": "Publication year",
    "is_free": "Free listing",
    "is_ku": "Kindle Unlimited",
    "reviews_recorded": "Reviews recorded",
    "has_pub_date": "Has publication date",
    "category": "Category",
    "publisher_group": "Publisher group",
}


def features(df: pd.DataFrame) -> pd.DataFrame:
    X = pd.DataFrame(index=df.index)
    X["log_price"] = np.log1p(df["price"])
    X["stars"] = df["stars"]
    X["log_reviews"] = np.log1p(df["reviews"])
    X["pub_year"] = df["pub_year"]
    for c in ["is_free", "is_ku", "reviews_recorded"]:
        X[c] = df[c].astype(int)
    X["has_pub_date"] = df["pub_year"].notna().astype(int)
    X["category"] = df["category"].astype(str)
    X["publisher_group"] = df["publisher_group"].astype(str)
    return X


def logistic_pipeline():
    pre = ColumnTransformer(
        [
            ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUMERIC),
            ("bin", "passthrough", BINARY),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ]
    )
    return Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=2000, C=1.0))])


def gbm_pipeline():
    pre = ColumnTransformer(
        [
            ("num", "passthrough", NUMERIC + BINARY),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
        ]
    )
    clf = HistGradientBoostingClassifier(
        learning_rate=0.06, max_iter=400, max_leaf_nodes=31, min_samples_leaf=40,
        l2_regularization=1.0, early_stopping=True, validation_fraction=0.1, random_state=SEED,
    )
    return Pipeline([("pre", pre), ("clf", clf)])


def precision_at(y, p, frac):
    k = max(1, int(round(len(y) * frac)))
    idx = np.argsort(-p)[:k]
    return float(np.mean(y[idx]))


def scores(y, p):
    return {
        "pr_auc": float(average_precision_score(y, p)),
        "roc_auc": float(roc_auc_score(y, p)),
        "precision_top1pct": precision_at(y, p, 0.01),
        "recall_top5pct": float(y[np.argsort(-p)[: int(round(len(y) * 0.05))]].sum() / y.sum()),
    }


def evaluate(df: pd.DataFrame, n_splits: int = 5):
    X = features(df)
    y = df["is_bestseller"].astype(int).to_numpy()
    groups = df["book_key"].to_numpy()
    cv = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=SEED)

    models = {
        "baseline": lambda: DummyClassifier(strategy="prior"),
        "logistic": logistic_pipeline,
        "gbm": gbm_pipeline,
    }
    fold_scores = {m: [] for m in models}
    oof = {m: np.zeros(len(y)) for m in models}
    for tr, te in cv.split(X, y, groups):
        assert not set(groups[tr]) & set(groups[te]), "book leaked across split"
        for name, make in models.items():
            m = make().fit(X.iloc[tr], y[tr])
            p = m.predict_proba(X.iloc[te])[:, 1]
            if name == "baseline":  # random ranking for a fair no-skill reference
                p = np.random.default_rng(SEED).random(len(te))
            oof[name][te] = p
            fold_scores[name].append(scores(y[te], p))

    summary = {}
    for name, rows in fold_scores.items():
        keys = rows[0].keys()
        summary[name] = {k: {"mean": float(np.mean([r[k] for r in rows])), "std": float(np.std([r[k] for r in rows]))} for k in keys}

    return {
        "n_listings": int(len(y)),
        "n_bestsellers": int(y.sum()),
        "prevalence": float(y.mean()),
        "always_no_accuracy": float(1 - y.mean()),
        "folds": n_splits,
        "cv": "StratifiedGroupKFold grouped by book (title + author)",
        "models": summary,
    }, oof


def importance(df: pd.DataFrame):
    """Permutation importance of the GBM on one held-out, book-grouped split."""
    X = features(df)
    y = df["is_bestseller"].astype(int).to_numpy()
    groups = df["book_key"].to_numpy()
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    tr, te = next(cv.split(X, y, groups))
    m = gbm_pipeline().fit(X.iloc[tr], y[tr])
    r = permutation_importance(
        m, X.iloc[te], y[te], scoring="average_precision", n_repeats=5, random_state=SEED, n_jobs=-1
    )
    out = [
        {"feature": LABELS[f], "importance": float(mu), "std": float(sd)}
        for f, mu, sd in zip(X.columns, r.importances_mean, r.importances_std)
    ]
    return sorted(out, key=lambda d: -d["importance"])


def fit_logistic_for_web(df: pd.DataFrame):
    """Fit the logistic model on all data and export it so the dashboard can
    score a hypothetical listing in the browser with the exact same maths."""
    X = features(df)
    y = df["is_bestseller"].astype(int).to_numpy()
    pipe = logistic_pipeline().fit(X, y)
    pre = pipe.named_steps["pre"]
    clf = pipe.named_steps["clf"]
    num = pre.named_transformers_["num"]
    ohe = pre.named_transformers_["cat"]
    coefs = clf.coef_[0]
    n_num, n_bin = len(NUMERIC), len(BINARY)
    cats = {}
    offset = n_num + n_bin
    for col, levels in zip(CATEGORICAL, ohe.categories_):
        cats[col] = {str(lv): float(coefs[offset + i]) for i, lv in enumerate(levels)}
        offset += len(levels)
    return {
        "intercept": float(clf.intercept_[0]),
        "numeric": {
            f: {
                "median": float(num.named_steps["imp"].statistics_[i]),
                "mean": float(num.named_steps["sc"].mean_[i]),
                "scale": float(num.named_steps["sc"].scale_[i]),
                "coef": float(coefs[i]),
            }
            for i, f in enumerate(NUMERIC)
        },
        "binary": {f: float(coefs[n_num + i]) for i, f in enumerate(BINARY)},
        "categorical": cats,
        "prevalence": float(y.mean()),
    }, pipe
