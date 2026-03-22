"""DataFrame filtering and sampling utilities.

These functions operate on in-memory DataFrames. They are synchronous
and safe to call from Textual worker threads.
"""

from __future__ import annotations

import pandas as pd


def filter_dataframe(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Filter a DataFrame using a pandas query string.

    Args:
        df: The source DataFrame.
        query: A pandas-compatible query string (e.g. "label == 'support'").

    Returns:
        A filtered DataFrame. Returns empty DataFrame if no rows match.
    """
    if not query or not query.strip():
        return df.copy()
    try:
        return df.query(query).reset_index(drop=True)
    except Exception:
        # Malformed query — return empty DataFrame rather than crashing
        return df.iloc[0:0].copy()


def sample_dataframe(df: pd.DataFrame, n: int, seed: int | None = None) -> pd.DataFrame:
    """Return a random sample of at most n rows from a DataFrame.

    Args:
        df: The source DataFrame.
        n: Number of rows to sample. If n >= len(df), all rows are returned.
        seed: Optional random seed for reproducibility.

    Returns:
        A DataFrame with at most n rows.
    """
    actual_n = min(n, len(df))
    if actual_n <= 0:
        return df.iloc[0:0].copy()
    return df.sample(n=actual_n, random_state=seed).reset_index(drop=True)
