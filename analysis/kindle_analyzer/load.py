"""Load the raw Kindle CSV with explicit types."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_CSV = ROOT / "data" / "raw" / "kindle_data-v2.csv"

DTYPES = {
    "asin": "string",
    "title": "string",
    "author": "string",
    "soldBy": "string",
    "imgUrl": "string",
    "productURL": "string",
    "stars": "float64",
    "reviews": "int64",
    "price": "float64",
    "isKindleUnlimited": "bool",
    "category_id": "int64",
    "isBestSeller": "bool",
    "isEditorsPick": "bool",
    "isGoodReadsChoice": "bool",
    "publishedDate": "string",
    "category_name": "string",
}


def load_raw(path: Path = RAW_CSV) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Download 'Amazon Kindle Books Dataset 2023' from Kaggle "
            "and place kindle_data-v2.csv in data/raw/ (see data/README.md)."
        )
    df = pd.read_csv(path, dtype=DTYPES)
    expected = set(DTYPES)
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing expected columns: {sorted(missing)}")
    return df
