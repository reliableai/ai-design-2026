"""Dataset fetchers for the Review & Judge tool.

All functions are synchronous and designed to be called from Textual
@work(thread=True) workers — never call them directly from async handlers.
"""

from __future__ import annotations

import pandas as pd


class KaggleCredentialsError(Exception):
    """Raised when Kaggle credentials are missing or invalid."""


def _get_kaggle_api():
    """Lazy import of kaggle API to avoid eager authentication on import."""
    try:
        import kaggle  # noqa: F401
        from kaggle.api.kaggle_api_extended import KaggleApiExtended

        api = KaggleApiExtended()
        api.authenticate()
        return api
    except OSError as exc:
        raise KaggleCredentialsError(
            "Kaggle credentials missing. Set KAGGLE_USERNAME and KAGGLE_KEY "
            "environment variables, or place kaggle.json in ~/.kaggle/."
        ) from exc


def load_hf_dataset(dataset_id: str, split: str = "train") -> pd.DataFrame:
    """Load a HuggingFace dataset and return it as a pandas DataFrame.

    Args:
        dataset_id: HuggingFace dataset identifier (e.g. 'bitext/...')
        split: Dataset split to load (default: 'train')

    Returns:
        DataFrame with all columns from the dataset.
    """
    import datasets  # lazy: avoid slow import at startup

    ds = datasets.load_dataset(dataset_id, split=split)
    return ds.to_pandas()


def load_twitter_dataset() -> pd.DataFrame:
    """Load the Twitter customer support dataset via the Kaggle API.

    Raises:
        KaggleCredentialsError: If Kaggle credentials are not configured.

    Returns:
        DataFrame with tweet text and metadata.
    """
    import os
    import zipfile
    import tempfile

    try:
        api = _get_kaggle_api()  # raises KaggleCredentialsError if creds missing
    except OSError as exc:
        raise KaggleCredentialsError(
            "Kaggle credentials missing. Set KAGGLE_USERNAME and KAGGLE_KEY "
            "environment variables, or place kaggle.json in ~/.kaggle/."
        ) from exc

    with tempfile.TemporaryDirectory() as tmpdir:
        api.dataset_download_cli(
            "thoughtvector/customer-support-on-twitter",
            path=tmpdir,
            quiet=True,
        )
        # Kaggle downloads as a zip — unpack the CSV inside
        zip_path = os.path.join(tmpdir, "customer-support-on-twitter.zip")
        with zipfile.ZipFile(zip_path, "r") as zf:
            csv_name = next(n for n in zf.namelist() if n.endswith(".csv"))
            zf.extract(csv_name, tmpdir)
        return pd.read_csv(os.path.join(tmpdir, csv_name))
