import pytest
from unittest.mock import MagicMock, patch
import pandas as pd


@pytest.fixture
def sample_df():
    """Small deterministic DataFrame for testing data processing."""
    return pd.DataFrame(
        {
            "text": ["hello world", "support ticket", "billing issue"],
            "label": ["greeting", "support", "billing"],
        }
    )


@pytest.fixture
def mock_load_dataset(monkeypatch):
    """Patches datasets.load_dataset to return a tiny mock dataset.

    Uses `datasets.load_dataset` (not src.data.fetchers.load_dataset) so the
    patch works even when the fetcher uses a lazy per-call import.
    """
    mock_ds = MagicMock()
    mock_ds.to_pandas.return_value = pd.DataFrame(
        {
            "text": [f"sample text {i}" for i in range(5)],
            "label": [f"label_{i}" for i in range(5)],
        }
    )
    try:
        import datasets as _datasets

        monkeypatch.setattr(_datasets, "load_dataset", lambda *a, **kw: mock_ds)
    except (ModuleNotFoundError, AttributeError):
        # datasets library not available — skip patching
        pass
    return mock_ds


@pytest.fixture
def mock_kaggle(monkeypatch):
    """Patches kaggle import to prevent eager authentication crash."""
    mock_api = MagicMock()
    try:
        monkeypatch.setattr("src.data.fetchers._get_kaggle_api", lambda: mock_api)
    except (ModuleNotFoundError, AttributeError):
        # src.data.fetchers not yet implemented — patch applied when module exists (Wave 1+)
        pass
    return mock_api
