"""DatasetExplorerApp — entry point for the Review & Judge TUI."""

from __future__ import annotations

from textual.app import App, ComposeResult

from src.tui.screens.explorer import ExplorerScreen


class DatasetExplorerApp(App):
    """Main application: wraps ExplorerScreen as the initial view."""

    TITLE = "Review & Judge — Dataset Explorer"
    SCREENS = {"explorer": ExplorerScreen}

    def on_mount(self) -> None:
        self.push_screen("explorer")


def main() -> None:
    """CLI entrypoint (wired via pyproject.toml [project.scripts])."""
    app = DatasetExplorerApp()
    app.run()


if __name__ == "__main__":
    main()
