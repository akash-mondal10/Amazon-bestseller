"""Cleaning rules for the Kindle dataset.

Every rule records how many rows it touched, so the cleaning report is a
precise account of what changed and why.
"""

import re

import numpy as np
import pandas as pd

# Scrape date of the dataset; dates after it are pre-orders.
SCRAPE_DATE = pd.Timestamp("2023-10-31")

CATEGORY_FIXES = {"Arts & Photo graphy": "Arts & Photography"}

# Sellers normalised to publisher groups. Names in the raw data vary
# ("Simon and Schuster Digital Sales Inc" vs "Simon & Schuster Digital Sales Inc.").
PUBLISHER_PATTERNS = [
    ("Sold by Amazon.com", r"^amazon\.com services"),
    ("Big Five", r"penguin|random house|\bprh\b|hachette|harpercollins|harper collins|macmillan|simon (?:&|and) schuster"),
    ("Academic & professional", r"wiley|pearson|cengage|mcgraw|elsevier|springer|oxford university|cambridge university|taylor|sage|wolters"),
]


def publisher_group(seller) -> str:
    if seller is None or pd.isna(seller) or not str(seller).strip():
        return "Not listed"
    s = str(seller).lower()
    for group, pat in PUBLISHER_PATTERNS:
        if re.search(pat, s):
            return group
    return "Other publishers"


def normalise_key(title, author) -> str:
    t = re.sub(r"[^a-z0-9 ]", "", str(title).lower())
    a = re.sub(r"[^a-z0-9 ]", "", str(author).lower())
    return f"{' '.join(t.split())}|{' '.join(a.split())}"


def clean(raw: pd.DataFrame):
    df = raw.copy()
    report = {"raw_rows": int(len(df)), "steps": []}

    def step(name, rows, note):
        report["steps"].append({"step": name, "rows_affected": int(rows), "note": note})

    # 1. Exact duplicate listings (same ASIN)
    n = int(df.duplicated("asin").sum())
    df = df.drop_duplicates("asin")
    step("Drop duplicate ASINs", n, "Same Amazon listing scraped twice.")

    # 2. Text tidy-up
    for c in ["title", "author", "category_name", "soldBy"]:
        df[c] = df[c].str.strip()
    n = int(df["category_name"].isin(CATEGORY_FIXES).sum())
    df["category_name"] = df["category_name"].replace(CATEGORY_FIXES)
    step("Fix category typo", n, "'Arts & Photo graphy' renamed to 'Arts & Photography'.")

    n = int(df["author"].isna().sum())
    df["author"] = df["author"].fillna("Unknown author")
    step("Fill missing authors", n, "Kept the listing, author set to 'Unknown author'.")

    # 3. Ratings: 0 stars means the book has no ratings yet, not a 0-star score.
    n = int((df["stars"] == 0).sum())
    df["stars"] = df["stars"].replace(0, np.nan)
    step("Unrated books", n, "stars = 0 treated as 'no rating yet' (missing), not a score of 0.")

    # 4. Reviews: in many categories the scraper recorded 0 reviews for books that
    # do have star ratings, which is impossible. Treat those as not recorded.
    bad = (df["reviews"] == 0) & df["stars"].notna()
    df["reviews_recorded"] = ~bad
    df["reviews"] = df["reviews"].astype("float64").where(~bad)
    step(
        "Review counts not recorded",
        int(bad.sum()),
        "reviews = 0 on a rated book is impossible, so treated as missing. "
        "This affects whole categories where the scraper did not capture reviews.",
    )

    # 5. Prices
    df["is_free"] = df["price"] == 0
    step("Free books flagged", int(df["is_free"].sum()), "price = 0 kept as free listings, flagged is_free.")

    # 6. Publication dates
    dt = pd.to_datetime(df["publishedDate"], errors="coerce")
    n_missing = int(dt.isna().sum())
    df["published"] = dt
    df["pub_year"] = dt.dt.year.astype("float64")
    df["is_preorder"] = dt > SCRAPE_DATE
    step("Missing publication date", n_missing, "Left missing; year-based charts use dated listings only.")
    step("Pre-orders flagged", int(df["is_preorder"].sum()), "Published after the October 2023 scrape.")

    # 7. Publishers
    df["publisher_group"] = df["soldBy"].map(publisher_group)
    step(
        "Seller names grouped",
        int(df["soldBy"].notna().sum()),
        f"{raw['soldBy'].nunique()} seller names grouped into {df['publisher_group'].nunique()} publisher groups.",
    )

    # 7b. Badges: Amazon shows at most one badge per listing.
    badge_count = df[["isBestSeller", "isEditorsPick", "isGoodReadsChoice"]].sum(axis=1)
    step(
        "One badge per listing",
        int((badge_count > 1).sum()),
        f"{int((badge_count == 1).sum()):,} listings show a badge and none show two, so Editors' Pick and "
        "Goodreads Choice listings never show Best Seller. Those flags are kept out of the model.",
    )

    # 8. Same book, several listings (editions, formats, categories)
    df["book_key"] = [normalise_key(t, a) for t, a in zip(df["title"], df["author"])]
    n = int(df.duplicated("book_key").sum())
    step(
        "Repeat listings of the same book",
        n,
        "Kept, because each listing has its own price, category and badge; "
        "used to keep a book's listings on one side of the train/test split.",
    )

    df = df.rename(
        columns={
            "isKindleUnlimited": "is_ku",
            "isBestSeller": "is_bestseller",
            "isEditorsPick": "is_editors_pick",
            "isGoodReadsChoice": "is_goodreads_choice",
            "category_name": "category",
        }
    )
    report["clean_rows"] = int(len(df))
    report["unique_books"] = int(df["book_key"].nunique())
    return df.reset_index(drop=True), report
