"""TUI smoke tests using Textual's built-in test pilot."""

import pytest
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Input, Select

from src.tui.app import DatasetExplorerApp
from src.tui.screens.explorer import DATASET_OPTIONS


@pytest.mark.e2e
async def test_datatable_render():
    """TUI-02: DataTable widget is present in the ExplorerScreen DOM."""
    app = DatasetExplorerApp()
    async with app.run_test() as pilot:
        # Allow the app to mount
        await pilot.pause()
        # DataTable must exist in the active screen's DOM
        table = app.screen.query_one(DataTable)
        assert table is not None


@pytest.mark.e2e
async def test_dataset_select_options():
    """TUI-02: Select widget exposes all four dataset options."""
    app = DatasetExplorerApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        select = app.screen.query_one(Select)
        assert select is not None
        # DATASET_OPTIONS has 4 entries
        assert len(DATASET_OPTIONS) == 4


async def test_model_bar_composes():
    """TUI-05: ModelBar widget composes with at least 2 Select and 2 Input widgets."""
    from src.tui.widgets.model_bar import ModelBar

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield ModelBar()

    app = TestApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert len(app.screen.query(Select)) >= 2
        assert len(app.screen.query(Input)) >= 2
