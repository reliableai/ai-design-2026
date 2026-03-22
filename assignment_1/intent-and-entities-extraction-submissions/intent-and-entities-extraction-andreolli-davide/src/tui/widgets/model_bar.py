"""ModelBar widget: model selectors for extractor and judge LLMs."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input, Label, Select

MODEL_OPTIONS: list[tuple[str, str]] = [
    ("Gemini 2.0 Flash", "gemini/gemini-2.0-flash"),
    ("Gemini 1.5 Pro", "gemini/gemini-1.5-pro"),
    ("GPT-4o Mini", "gpt-4o-mini"),
    ("GPT-4o", "gpt-4o"),
    ("Claude 3.5 Haiku", "claude-3-5-haiku-20241022"),
    ("Claude 3.5 Sonnet", "claude-3-5-sonnet-20241022"),
]


class ModelBar(Widget):
    """Horizontal bar for extractor and judge model selection."""

    DEFAULT_CSS = """
    ModelBar {
        height: auto;
        layout: horizontal;
        padding: 0 1;
    }
    ModelBar Label {
        width: 12;
        content-align: center middle;
    }
    ModelBar Select {
        width: 30;
    }
    ModelBar Input {
        width: 22;
        margin-left: 1;
    }
    """

    class Changed(Message):
        """Posted when either model selection changes."""

        def __init__(self, extractor_model: str, judge_model: str) -> None:
            super().__init__()
            self.extractor_model = extractor_model
            self.judge_model = judge_model

    def compose(self) -> ComposeResult:
        yield Label("Extractor:")
        yield Select(
            options=MODEL_OPTIONS,
            prompt="Select extractor model\u2026",
            id="extractor-select",
        )
        yield Input(placeholder="or type custom model\u2026", id="extractor-custom")
        yield Label("Judge:")
        yield Select(
            options=MODEL_OPTIONS,
            prompt="Select judge model\u2026",
            id="judge-select",
        )
        yield Input(placeholder="or type custom model\u2026", id="judge-custom")

    def _get_extractor_model(self) -> str:
        sel = self.query_one("#extractor-select", Select)
        if sel.value and sel.value is not Select.BLANK:
            return str(sel.value)
        return self.query_one("#extractor-custom", Input).value.strip()

    def _get_judge_model(self) -> str:
        sel = self.query_one("#judge-select", Select)
        if sel.value and sel.value is not Select.BLANK:
            return str(sel.value)
        return self.query_one("#judge-custom", Input).value.strip()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.value and event.value is not Select.BLANK:
            self.post_message(
                self.Changed(self._get_extractor_model(), self._get_judge_model())
            )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(
            self.Changed(self._get_extractor_model(), self._get_judge_model())
        )
