import pytest
import pandas as pd
from src.data.fetchers import (
    load_hf_dataset,
    load_twitter_dataset,
    KaggleCredentialsError,
)
from src.data.processing import filter_dataframe, sample_dataframe


def test_load_bitext(mock_load_dataset):
    """DATA-01: load_hf_dataset returns a DataFrame for the Bitext dataset."""
    df = load_hf_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_tobibueck(mock_load_dataset):
    """DATA-02: load_hf_dataset returns a DataFrame for the Tobi-Bueck dataset."""
    df = load_hf_dataset("Tobi-Bueck/customer-support-tickets")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_cfpb(mock_load_dataset):
    """DATA-03: load_hf_dataset returns a DataFrame for the CFPB dataset."""
    df = load_hf_dataset("CFPB/consumer-finance-complaints")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_twitter_success(mock_kaggle):
    """DATA-04 (happy path): load_twitter_dataset returns DataFrame when creds present."""
    # mock_kaggle patches _get_kaggle_api; simulate a downloaded CSV
    import os, tempfile, zipfile, io
    import pandas as pd
    from unittest.mock import patch

    sample_csv = "author_id,text\n1,hello\n2,world\n"

    def fake_download(dataset_slug, path, quiet):
        zip_path = os.path.join(path, "customer-support-on-twitter.zip")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("twcs.csv", sample_csv)
        with open(zip_path, "wb") as f:
            f.write(buf.getvalue())

    mock_kaggle.dataset_download_cli.side_effect = fake_download
    df = load_twitter_dataset()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_load_twitter_missing_creds(monkeypatch):
    """DATA-04 (missing creds): load_twitter_dataset raises KaggleCredentialsError."""
    from src.data import fetchers

    def raise_os_error():
        raise OSError("kaggle.json not found")

    monkeypatch.setattr(fetchers, "_get_kaggle_api", raise_os_error)
    with pytest.raises(KaggleCredentialsError):
        load_twitter_dataset()


def test_filter_matching_rows(sample_df):
    """DATA-05: filter_dataframe returns only rows matching the query."""
    result = filter_dataframe(sample_df, "label == 'greeting'")
    assert len(result) == 1
    assert result.iloc[0]["label"] == "greeting"


def test_filter_no_match(sample_df):
    """DATA-05: filter_dataframe returns empty DataFrame when no rows match."""
    result = filter_dataframe(sample_df, "label == 'nonexistent'")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


def test_sample_n(sample_df):
    """DATA-05: sample_dataframe returns exactly n rows."""
    result = sample_dataframe(sample_df, n=2)
    assert len(result) == 2


def test_sample_exceeds_length(sample_df):
    """DATA-05: sample_dataframe returns all rows when n > len(df)."""
    result = sample_dataframe(sample_df, n=999)
    assert len(result) == len(sample_df)


def test_sample_reproducible(sample_df):
    """DATA-05: sample_dataframe with same seed returns same rows."""
    r1 = sample_dataframe(sample_df, n=2, seed=42)
    r2 = sample_dataframe(sample_df, n=2, seed=42)
    pd.testing.assert_frame_equal(r1, r2)
