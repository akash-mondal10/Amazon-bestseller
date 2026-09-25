"""Checks for the cleaning rules and the leakage guard.

Run from the repo root:  python -m pytest -q
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))

from kindle_analyzer.clean import clean, publisher_group  # noqa: E402
from kindle_analyzer.model import features  # noqa: E402


def raw(**over):
    row = {
        "asin": "B000000001", "title": "A Book", "author": "An Author", "soldBy": "Amazon.com Services LLC",
        "imgUrl": "", "productURL": "", "stars": 4.5, "reviews": 120, "price": 4.99,
        "isKindleUnlimited": True, "category_id": 1, "isBestSeller": False, "isEditorsPick": False,
        "isGoodReadsChoice": False, "publishedDate": "2021-05-01", "category_name": "Romance",
    }
    row.update(over)
    return row


def frame(*rows):
    return pd.DataFrame(list(rows))


def test_zero_stars_means_unrated():
    df, _ = clean(frame(raw(stars=0.0, reviews=0)))
    assert np.isnan(df.loc[0, "stars"])
    assert df.loc[0, "reviews_recorded"]  # 0 reviews on an unrated book is plausible


def test_zero_reviews_on_rated_book_is_missing():
    df, rep = clean(frame(raw(stars=4.6, reviews=0), raw(asin="B2", stars=4.6, reviews=10)))
    assert np.isnan(df.loc[0, "reviews"]) and not df.loc[0, "reviews_recorded"]
    assert df.loc[1, "reviews"] == 10
    step = next(s for s in rep["steps"] if s["step"] == "Review counts not recorded")
    assert step["rows_affected"] == 1


def test_category_typo_fixed():
    df, _ = clean(frame(raw(category_name="Arts & Photo graphy")))
    assert df.loc[0, "category"] == "Arts & Photography"


def test_publisher_groups():
    assert publisher_group("Simon and Schuster Digital Sales Inc") == "Big Five"
    assert publisher_group("Simon & Schuster Digital Sales Inc.") == "Big Five"
    assert publisher_group("PRH UK") == "Big Five"
    assert publisher_group("JOHN WILEY AND SONS INC") == "Academic & professional"
    assert publisher_group("Amazon.com Services LLC") == "Sold by Amazon.com"
    assert publisher_group(None) == "Not listed"
    assert publisher_group("Yen Press LLC") == "Other publishers"


def test_same_book_shares_a_key():
    df, _ = clean(frame(raw(title="1984", author="George Orwell"), raw(asin="B2", title="1984 ", author="george orwell")))
    assert df.loc[0, "book_key"] == df.loc[1, "book_key"]


def test_badge_flags_not_model_features():
    df, _ = clean(frame(raw()))
    cols = set(features(df).columns)
    assert "is_editors_pick" not in cols and "is_goodreads_choice" not in cols
