"""ExplorerScreen — the primary dataset exploration view."""

from __future__ import annotations

import pandas as pd
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Label, LoadingIndicator, Select

from src.tui.widgets.filter_bar import FilterBar

# Dataset options shown in the selector
DATASET_OPTIONS: list[tuple[str, str]] = [
    (
        "Bitext (Customer Support)",
        "bitext/Bitext-customer-support-llm-chatbot-training-dataset",
    ),
    ("Tobi-Bueck (Support Tickets)", "Tobi-Bueck/customer-support-tickets"),
    ("CFPB (Consumer Complaints)", "CFPB/consumer-finance-complaints"),
    ("Twitter (Kaggle — requires credentials)", "twitter"),
]

DEFAULT_SAMPLE_SIZE = 100


class ExplorerScreen(Screen):
    """Main exploration view: dataset selector + data grid."""

    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("r", "refresh_data", "Refresh / resample"),
    ]

    CSS = """
    ExplorerScreen {
        layout: vertical;
    }
    #selector-row {
        height: 3;
        layout: horizontal;
        padding: 0 1;
    }
    #dataset-select {
        width: 1fr;
    }
    #status-label {
        height: 1;
        padding: 0 1;
        color: $text-muted;
    }
    LoadingIndicator {
        height: 3;
    }
    DataTable {
        height: 1fr;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._current_df: pd.DataFrame | None = None
        self._current_full_df: pd.DataFrame | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Select(
            options=DATASET_OPTIONS,
            prompt="Select a dataset…",
            id="dataset-select",
        )
        yield FilterBar()
        yield Label("No dataset loaded.", id="status-label")
        yield LoadingIndicator()
        yield DataTable(zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        # Hide loading indicator until a fetch is in progress
        self.query_one(LoadingIndicator).display = False

    def on_select_changed(self, event: Select.Changed) -> None:
        """Trigger data load when the user picks a dataset."""
        if event.value and event.value is not Select.BLANK:
            self._load_dataset(str(event.value))

    def action_refresh_data(self) -> None:
        """Re-sample the current dataset (keybind: r)."""
        select = self.query_one(Select)
        if select.value and select.value is not Select.BLANK:
            self._load_dataset(str(select.value))

    def on_filter_bar_applied(self, event: FilterBar.Applied) -> None:
        """Apply a query filter to the in-memory DataFrame."""
        if self._current_full_df is None:
            return
        from src.data.processing import filter_dataframe, sample_dataframe

        filtered = filter_dataframe(self._current_full_df, event.query)
        sample = sample_dataframe(filtered, n=DEFAULT_SAMPLE_SIZE)
        self._update_table(sample, success=True)

    def on_filter_bar_resampled(self, _: FilterBar.Resampled) -> None:
        """Re-sample the current full DataFrame."""
        if self._current_full_df is None:
            return
        from src.data.processing import sample_dataframe

        sample = sample_dataframe(self._current_full_df, n=DEFAULT_SAMPLE_SIZE)
        self._update_table(sample, success=True)

    @work(thread=True, exclusive=True)
    def _load_dataset(self, dataset_id: str) -> None:
        """Background worker: fetch data and push to DataTable.

        Runs off the main thread to prevent UI freeze.
        """
        from src.data.fetchers import (
            KaggleCredentialsError,
            load_hf_dataset,
            load_twitter_dataset,
        )
        from src.data.processing import sample_dataframe

        self.call_from_thread(self._set_loading, True)

        try:
            if dataset_id == "twitter":
                df = load_twitter_dataset()
            else:
                df = load_hf_dataset(dataset_id)

            # Store full DataFrame for filter/resample operations (thread-safe assignment)
            self.call_from_thread(setattr, self, "_current_full_df", df)
            sample = sample_dataframe(df, n=DEFAULT_SAMPLE_SIZE)
            self.call_from_thread(self._update_table, sample, success=True)

        except KaggleCredentialsError:
            self.call_from_thread(
                self._show_error,
                "Twitter dataset requires Kaggle credentials.\n"
                "Set KAGGLE_USERNAME and KAGGLE_KEY environment variables.",
            )
        except Exception as exc:  # noqa: BLE001
            self.call_from_thread(self._show_error, f"Failed to load dataset: {exc}")

    def _set_loading(self, is_loading: bool) -> None:
        """Toggle loading indicator visibility (must run on main thread)."""
        loader = self.query_one(LoadingIndicator)
        loader.display = is_loading
        table = self.query_one(DataTable)
        table.display = not is_loading

    def _update_table(self, df: pd.DataFrame, *, success: bool) -> None:
        """Populate the DataTable with sampled rows (must run on main thread)."""
        self._set_loading(False)
        table = self.query_one(DataTable)
        table.clear(columns=True)
        if not df.empty:
            table.add_columns(*df.columns.tolist())
            table.add_rows(df.itertuples(index=False, name=None))
        label = self.query_one("#status-label", Label)
        label.update(f"Showing {len(df)} rows.")

    def _show_error(self, message: str) -> None:
        """Display an error notification (must run on main thread)."""
        self._set_loading(False)
        self.app.notify(message, severity="error", timeout=10)
        label = self.query_one("#status-label", Label)
        label.update(f"Error: {message.splitlines()[0]}")
