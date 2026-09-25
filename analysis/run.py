"""Run the full pipeline: load -> clean -> analyse -> model -> figures -> export.

    python analysis/run.py

Writes reports/ (JSON + PNG charts) and web/public/data/ (what the dashboard reads).
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from kindle_analyzer import analyze, clean, figures, model  # noqa: E402
from kindle_analyzer.load import ROOT, load_raw  # noqa: E402

REPORTS = ROOT / "reports"
WEB_DATA = ROOT / "web" / "public" / "data"


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, separators=(",", ":"), ensure_ascii=False, allow_nan=False))


def r(x, n=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def books_payload(df, cat_index):
    """Compact columnar table for the book explorer, one file per category."""
    b = lambda c: df[c].to_numpy(dtype=np.int64)
    flags = b("is_bestseller") | (b("is_ku") << 1) | (b("is_editors_pick") << 2) | (b("is_goodreads_choice") << 3)
    return {
        "asin": df["asin"].tolist(),
        "title": [t if len(t) <= 160 else t[:157] + "..." for t in df["title"].astype(str)],
        "author": df["author"].astype(str).tolist(),
        "price": [r(v, 2) for v in df["price"]],
        "stars": [r(v, 1) for v in df["stars"]],
        "reviews": [None if np.isnan(v) else int(v) for v in df["reviews"]],
        "year": [None if np.isnan(v) else int(v) for v in df["pub_year"]],
        "flags": flags.tolist(),
        "category": [cat_index[c] for c in df["category"]],
    }


def main():
    t0 = time.time()
    print("Loading raw data...")
    raw = load_raw()
    df, cleaning = clean.clean(raw)
    print(f"  {cleaning['raw_rows']:,} rows -> {cleaning['clean_rows']:,} listings, {cleaning['unique_books']:,} unique books")

    print("Evaluating models (5-fold grouped CV)...")
    model_summary, _ = model.evaluate(df)
    for name, s in model_summary["models"].items():
        print(f"  {name:9s} PR-AUC {s['pr_auc']['mean']:.3f}  ROC-AUC {s['roc_auc']['mean']:.3f}  "
              f"top-1% precision {s['precision_top1pct']['mean']:.3f}")
    print("Permutation importance...")
    imp = model.importance(df)
    web_model, _ = model.fit_logistic_for_web(df)

    print("Aggregating...")
    cats = analyze.category_table(df)
    overall = analyze.scope_summary(df)
    scopes = {"All": overall}
    for c in cats:
        scopes[c["category"]] = analyze.scope_summary(df[df["category"] == c["category"]])
    insights = analyze.insights(df, cats, model_summary)
    authors = analyze.top_authors(df)

    print("Drawing report charts...")
    figs = figures.make_all(df, overall, cats, model_summary, imp, REPORTS / "figures")

    print("Exporting...")
    write(REPORTS / "cleaning_report.json", cleaning)
    write(REPORTS / "model_report.json", {**model_summary, "permutation_importance": imp})
    write(REPORTS / "insights.json", insights)

    cat_names = sorted(c["category"] for c in cats)
    cat_index = {c: i for i, c in enumerate(cat_names)}
    meta = {
        "source": {
            "name": "Amazon Kindle Books Dataset 2023",
            "author": "asaniczka (Kaggle)",
            "url": "https://www.kaggle.com/datasets/asaniczka/amazon-kindle-books-dataset-2023-130k-books",
            "scraped": "October 2023",
        },
        "categories": cat_names,
        "category_table": cats,
        "insights": insights,
        "top_authors": authors,
        "cleaning": cleaning,
        "model": {**model_summary, "permutation_importance": imp},
        "estimator": web_model,
        "figures": figs,
    }
    write(WEB_DATA / "meta.json", meta)
    write(WEB_DATA / "scopes.json", scopes)
    for c in cat_names:
        part = df[df["category"] == c]
        write(WEB_DATA / "books" / f"{cat_index[c]}.json", books_payload(part, cat_index))

    print(f"Done in {time.time() - t0:.0f}s. {len(figs)} charts in reports/figures.")


if __name__ == "__main__":
    main()
