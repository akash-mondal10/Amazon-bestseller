"""Aggregates behind the dashboard and the written insights.

Every aggregate is computed for the whole catalogue and for each category, so
the dashboard's category filter only switches between precomputed results.
"""

import numpy as np
import pandas as pd

PRICE_BANDS = [
    ("Free", -0.01, 0.0),
    ("Under $3", 0.0, 2.99),
    ("$3–4.99", 2.99, 4.99),
    ("$5–9.99", 4.99, 9.99),
    ("$10–14.99", 9.99, 14.99),
    ("$15–24.99", 14.99, 24.99),
    ("$25+", 24.99, np.inf),
]
STAR_BANDS = [("Under 4.0", 0, 3.95), ("4.0–4.3", 3.95, 4.35), ("4.4–4.6", 4.35, 4.65), ("4.7–5.0", 4.65, 5.01)]
YEARS = list(range(2000, 2024))


def _rate(s):
    return float(s.mean()) if len(s) else None


def _band(values, bands):
    out = pd.Series(pd.NA, index=values.index, dtype="object")
    for label, lo, hi in bands:
        out[(values > lo) & (values <= hi)] = label
    return out


def scope_summary(d: pd.DataFrame) -> dict:
    bs = d["is_bestseller"]
    # Only trust review figures where the scraper captured most review counts.
    rec = d[d["reviews_recorded"]] if d["reviews_recorded"].mean() >= 0.5 else d.iloc[0:0]
    kpis = {
        "listings": int(len(d)),
        "unique_books": int(d["book_key"].nunique()),
        "bestsellers": int(bs.sum()),
        "bestseller_rate": _rate(bs),
        "median_price": float(d["price"].median()),
        "avg_stars": float(d["stars"].mean()),
        "ku_share": _rate(d["is_ku"]),
        "free_share": _rate(d["is_free"]),
        "review_capture": _rate(d["reviews_recorded"]),
        "median_reviews": float(rec["reviews"].median()) if len(rec) else None,
        "median_reviews_bestseller": float(rec.loc[rec["is_bestseller"], "reviews"].median()) if rec["is_bestseller"].any() else None,
        "median_reviews_other": float(rec.loc[~rec["is_bestseller"], "reviews"].median()) if len(rec) else None,
    }

    price_band = _band(d["price"], PRICE_BANDS)
    price = [
        {"band": lab, "listings": int((price_band == lab).sum()),
         "bestsellers": int(bs[price_band == lab].sum()), "rate": _rate(bs[price_band == lab])}
        for lab, _, _ in PRICE_BANDS
    ]

    star_band = _band(d["stars"].fillna(-1), STAR_BANDS)
    stars = [
        {"band": lab, "listings": int((star_band == lab).sum()), "rate": _rate(bs[star_band == lab])}
        for lab, _, _ in STAR_BANDS
    ] + [{"band": "Unrated", "listings": int(d["stars"].isna().sum()), "rate": _rate(bs[d["stars"].isna()])}]

    ku = [
        {"label": "Kindle Unlimited", "listings": int(d["is_ku"].sum()), "rate": _rate(bs[d["is_ku"]])},
        {"label": "Not in KU", "listings": int((~d["is_ku"]).sum()), "rate": _rate(bs[~d["is_ku"]])},
    ]

    pub = (
        d.groupby("publisher_group")
        .agg(listings=("asin", "size"), bestsellers=("is_bestseller", "sum"), rate=("is_bestseller", "mean"))
        .reset_index().sort_values("listings", ascending=False)
    )
    publishers = [
        {"group": r.publisher_group, "listings": int(r.listings), "bestsellers": int(r.bestsellers), "rate": float(r.rate)}
        for r in pub.itertuples()
    ]

    dated = d[d["pub_year"].between(YEARS[0], YEARS[-1])]
    by_year = dated.groupby("pub_year").agg(listings=("asin", "size"), rate=("is_bestseller", "mean"))
    years = [
        {"year": y, "listings": int(by_year.loc[y, "listings"]) if y in by_year.index else 0,
         "rate": float(by_year.loc[y, "rate"]) if y in by_year.index else None}
        for y in YEARS
    ]

    return {"kpis": kpis, "price": price, "stars": stars, "ku": ku,
            "publishers": publishers, "years": years}


def category_table(df: pd.DataFrame) -> list:
    g = df.groupby("category").agg(
        listings=("asin", "size"),
        bestsellers=("is_bestseller", "sum"),
        rate=("is_bestseller", "mean"),
        median_price=("price", "median"),
        avg_stars=("stars", "mean"),
        ku_share=("is_ku", "mean"),
        review_capture=("reviews_recorded", "mean"),
    ).reset_index().sort_values("rate", ascending=False)
    return [
        {k: (float(v) if isinstance(v, (float, np.floating)) else (int(v) if isinstance(v, (int, np.integer)) else v))
         for k, v in row.items()}
        for row in g.to_dict("records")
    ]


def top_authors(df: pd.DataFrame, n: int = 12) -> list:
    known = df[df["author"] != "Unknown author"]
    g = known.groupby("author").agg(bestsellers=("is_bestseller", "sum"), listings=("asin", "size"))
    g = g[g["bestsellers"] > 0].sort_values(["bestsellers", "listings"], ascending=[False, True]).head(n)
    return [{"author": a, "bestsellers": int(r.bestsellers), "listings": int(r.listings)} for a, r in g.iterrows()]


def insights(df: pd.DataFrame, cats: list, model_summary: dict) -> list:
    s = scope_summary(df)
    k = s["kpis"]
    ku_in, ku_out = s["ku"][0]["rate"], s["ku"][1]["rate"]
    best_cat, worst_cat = cats[0], cats[-1]
    bands = [b for b in s["price"] if b["listings"] >= 1000]
    top_band = max(bands, key=lambda b: b["rate"])
    gbm = model_summary["models"]["gbm"]
    lift = gbm["precision_top1pct"]["mean"] / model_summary["prevalence"]
    no_reviews = [c["category"] for c in cats if c["review_capture"] < 0.5]
    fmt = lambda x: f"{x * 100:.1f}%"
    by_cat = df.groupby(["category", "is_ku"])["is_bestseller"].mean().unstack()
    ku_wins = int((by_cat[True] > by_cat[False]).sum())
    return [
        f"{k['bestsellers']:,} of {k['listings']:,} listings ({fmt(k['bestseller_rate'])}) carry Amazon's Best Seller badge.",
        f"Kindle Unlimited books carry the badge {ku_in / ku_out:.1f}× as often as other books ({fmt(ku_in)} vs {fmt(ku_out)}), "
        f"and the gap holds in {ku_wins} of {len(cats)} categories.",
        f"{best_cat['category']} has the highest badge rate ({fmt(best_cat['rate'])}); {worst_cat['category']} the lowest ({fmt(worst_cat['rate'])}).",
        f"Among price bands, {top_band['band']} has the highest badge rate ({fmt(top_band['rate'])}); the median listing costs ${k['median_price']:.2f}.",
        f"Where review counts were recorded, bestsellers have a median of {k['median_reviews_bestseller']:,.0f} reviews vs {k['median_reviews_other']:,.0f} for other books.",
        f"Ratings barely separate books: the average listing scores {k['avg_stars']:.2f} stars.",
        f"Review counts are missing for most books in {len(no_reviews)} of {len(cats)} categories (a scraping gap), so review figures use recorded counts only.",
        f"The model's top 1% of listings are bestsellers {fmt(gbm['precision_top1pct']['mean'])} of the time, {lift:.0f}× the {fmt(model_summary['prevalence'])} base rate.",
    ]
