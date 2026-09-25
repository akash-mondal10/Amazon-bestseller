"""Static report charts (Matplotlib + Seaborn), saved to reports/figures."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import seaborn as sns  # noqa: E402

INK = "#1f2430"
ACCENT = "#e07a1f"
MUTED = "#9aa3b2"


def _style():
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update({
        "axes.edgecolor": "#d6dae1", "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
        "axes.titleweight": "bold", "axes.titlesize": 13, "figure.dpi": 110, "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def _pct_axis(ax, axis="x"):
    fmt = matplotlib.ticker.PercentFormatter(1.0, decimals=1)
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(fmt)


def category_rates(cats, out: Path, base_rate: float):
    fig, ax = plt.subplots(figsize=(8, 9))
    names = [c["category"] for c in cats][::-1]
    rates = [c["rate"] for c in cats][::-1]
    colors = [ACCENT if r >= base_rate else MUTED for r in rates]
    ax.barh(names, rates, color=colors)
    ax.axvline(base_rate, color=INK, ls="--", lw=1)
    ax.text(base_rate, len(names) - 0.3, f" overall {base_rate:.1%}", va="bottom", fontsize=9, color=INK)
    _pct_axis(ax)
    ax.set_title("Share of listings with the Best Seller badge, by category")
    ax.set_xlabel("Listings with the badge")
    fig.savefig(out / "01_bestseller_rate_by_category.png"); plt.close(fig)


def price_bands(price, out: Path):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.bar([b["band"] for b in price], [b["rate"] for b in price], color=ACCENT)
    for i, b in enumerate(price):
        ax.text(i, b["rate"], f"{b['rate']:.1%}\n{b['listings']:,} listings", ha="center", va="bottom", fontsize=8)
    _pct_axis(ax, "y")
    ax.set_ylim(0, max(b["rate"] for b in price) * 1.3)
    ax.set_title("Cheaper books carry the badge more often")
    ax.set_ylabel("Listings with the badge")
    fig.savefig(out / "02_bestseller_rate_by_price.png"); plt.close(fig)


def kindle_unlimited(df, out: Path):
    g = df.groupby(["category", "is_ku"])["is_bestseller"].mean().unstack().dropna()
    g = g.sort_values(True)
    fig, ax = plt.subplots(figsize=(8, 9))
    y = np.arange(len(g))
    ax.hlines(y, g[False], g[True], color="#d6dae1", lw=2)
    ax.scatter(g[False], y, color=MUTED, label="Not in Kindle Unlimited", zorder=3)
    ax.scatter(g[True], y, color=ACCENT, label="Kindle Unlimited", zorder=3)
    ax.set_yticks(y, g.index)
    _pct_axis(ax)
    ax.legend(loc="lower right", frameon=False)
    ax.set_title("Kindle Unlimited vs not, badge rate within each category")
    fig.savefig(out / "03_kindle_unlimited_by_category.png"); plt.close(fig)


def reviews(df, out: Path):
    rec = df[df["reviews_recorded"] & (df["reviews"] > 0)].copy()
    rec["Group"] = np.where(rec["is_bestseller"], "Best Seller", "Other")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    sns.kdeplot(data=rec, x=np.log10(rec["reviews"]), hue="Group", common_norm=False,
                fill=True, alpha=0.3, palette={"Best Seller": ACCENT, "Other": MUTED}, ax=ax)
    ticks = [0, 1, 2, 3, 4, 5]
    ax.set_xticks(ticks, [f"{10**t:,}" for t in ticks])
    ax.set_xlabel("Review count (log scale, categories where reviews were recorded)")
    ax.set_title("Bestsellers tend to have more reviews")
    fig.savefig(out / "04_reviews_bestseller_vs_other.png"); plt.close(fig)


def ratings(df, out: Path):
    rated = df[df["stars"].notna()]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    sns.histplot(rated["stars"], bins=np.arange(1, 5.1, 0.1), color=MUTED, ax=ax)
    ax.set_title(f"Ratings bunch up near the top: mean {rated['stars'].mean():.2f} stars")
    ax.set_xlabel("Star rating")
    fig.savefig(out / "05_rating_distribution.png"); plt.close(fig)


def years(years_data, out: Path):
    ys = [y for y in years_data if y["listings"] >= 200]
    fig, ax1 = plt.subplots(figsize=(8, 4.2))
    ax1.bar([y["year"] for y in ys], [y["listings"] for y in ys], color="#e6e9ee")
    ax1.set_ylabel("Listings published")
    ax2 = ax1.twinx()
    ax2.plot([y["year"] for y in ys], [y["rate"] for y in ys], color=ACCENT, marker="o", lw=2)
    _pct_axis(ax2, "y")
    ax2.set_ylabel("Badge rate")
    ax2.grid(False)
    ax1.set_title("Listings and badge rate by publication year")
    fig.savefig(out / "06_publication_year.png"); plt.close(fig)


def correlation(df, out: Path):
    cols = {"price": "Price", "stars": "Stars", "reviews": "Reviews", "pub_year": "Pub. year",
            "is_ku": "Kindle Unl.", "is_bestseller": "Best Seller"}
    d = df[list(cols)].astype(float).rename(columns=cols)
    corr = d.corr(method="spearman")
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, square=True, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Spearman correlations (pairwise, missing values excluded)")
    fig.savefig(out / "07_correlation_heatmap.png"); plt.close(fig)


def model_ranking(model_summary, out: Path):
    ms = model_summary["models"]
    names = {"baseline": "Random ranking", "logistic": "Logistic regression", "gbm": "Gradient boosting"}
    fig, ax = plt.subplots(figsize=(8, 3.6))
    vals = [ms[m]["precision_top1pct"]["mean"] for m in names]
    errs = [ms[m]["precision_top1pct"]["std"] for m in names]
    ax.barh(list(names.values()), vals, xerr=errs, color=[MUTED, "#c9b18f", ACCENT])
    for i, v in enumerate(vals):
        ax.text(v + 0.01, i, f"{v:.1%}", va="center", fontsize=9)
    _pct_axis(ax)
    ax.set_xlim(0, max(vals) * 1.3)
    ax.set_title("Share of Best Sellers in each model's top 1% (5-fold CV)")
    fig.savefig(out / "08_model_precision_top1pct.png"); plt.close(fig)


def feature_importance(imp, out: Path):
    imp = [r for r in imp if r["importance"] > 0.0005]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh([r["feature"] for r in imp][::-1], [r["importance"] for r in imp][::-1],
            xerr=[r["std"] for r in imp][::-1], color=ACCENT)
    ax.set_xlabel("Drop in PR-AUC when the feature is shuffled")
    ax.set_title("What the model relies on (permutation importance)")
    fig.savefig(out / "09_feature_importance.png"); plt.close(fig)


def make_all(df, summary, cats, model_summary, imp, out: Path):
    _style()
    out.mkdir(parents=True, exist_ok=True)
    base = summary["kpis"]["bestseller_rate"]
    category_rates(cats, out, base)
    price_bands(summary["price"], out)
    kindle_unlimited(df, out)
    reviews(df, out)
    ratings(df, out)
    years(summary["years"], out)
    correlation(df, out)
    model_ranking(model_summary, out)
    feature_importance(imp, out)
    return sorted(p.name for p in out.glob("*.png"))
