"""FilterBar widget: text filter input + resample button."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Input, Label


class FilterBar(Widget):
    """Horizontal bar with a pandas query input and a Resample button."""

    DEFAULT_CSS = """
    FilterBar {
        height: 3;
        layout: horizontal;
        padding: 0 1;
    }
    FilterBar Label {
        width: 8;
        content-align: center middle;
    }
    FilterBar Input {
        width: 1fr;
    }
    FilterBar Button {
        width: 14;
        margin-left: 1;
    }
    """

    class Applied(Message):
        """Posted when the user submits a filter query."""

        def __init__(self, query: str) -> None:
            super().__init__()
            self.query = query

    class Resampled(Message):
        """Posted when the user clicks the Resample button."""

    def compose(self) -> ComposeResult:
        yield Label("Filter:")
        yield Input(
            placeholder="pandas query, e.g.  label == 'billing'", id="filter-input"
        )
        yield Button("Resample", id="resample-btn", variant="primary")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(self.Applied(query=event.value.strip()))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "resample-btn":
            self.post_message(self.Resampled())
