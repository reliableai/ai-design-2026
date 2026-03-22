"""LLM-related unit tests: extractor, judge, analysis, batch, and ModelBar message."""

import pytest


@pytest.mark.xfail(strict=False, reason="not yet implemented")
def test_extract_row(mock_instructor_client):
    """EVAL-03: extract_row returns ExtractionResult with intent, sentiment, urgency."""
    try:
        from src.llm import extract_row
    except ImportError:
        pytest.xfail("src.llm not yet created")

    result = extract_row("My order hasn't arrived", "gpt-4o-mini")
    assert result.intent == "billing_issue"
    assert result.sentiment == "negative"
    assert result.urgency == "high"


@pytest.mark.xfail(strict=False, reason="not yet implemented")
def test_judge_row(mock_litellm):
    """EVAL-04: judge_row returns JudgeResult with .score (int 1-10) and .critique (str)."""
    try:
        from src.llm import judge_row
    except ImportError:
        pytest.xfail("src.llm not yet created")

    result = judge_row(
        "My order hasn't arrived", {"intent": "billing_issue"}, "gpt-4o-mini"
    )
    assert result.score == 8
    assert "Good" in result.critique


@pytest.mark.xfail(strict=False, reason="not yet implemented")
def test_analyse_batch(mock_litellm):
    """EVAL-05: analyse_batch returns FailureSummary with .aggregate_score and .failure_categories."""
    try:
        from src.llm import analyse_batch
    except ImportError:
        pytest.xfail("src.llm not yet created")

    # Configure mock to return JSON-parseable FailureSummary
    mock_litellm.choices[
        0
    ].message.content = '{"aggregate_score": 3.0, "failure_categories": ["wrong intent"], "examples": ["My order"]}'

    results = [
        {
            "text": "My order hasn't arrived",
            "extraction": {"intent": "billing_issue"},
            "score": 3,
            "critique": "Wrong category",
        }
    ]
    result = analyse_batch(results, "gpt-4o-mini")
    assert hasattr(result, "aggregate_score")
    assert hasattr(result, "failure_categories")


@pytest.mark.xfail(strict=False, reason="not yet implemented")
def test_batch_concurrency():
    """EVAL-03/04: batch worker calls extract+judge for each row, max 5 concurrent."""
    pytest.xfail("batch worker not yet implemented")


@pytest.mark.xfail(strict=False, reason="not yet implemented")
def test_model_bar_message():
    """TUI-05: ModelBar.Changed message carries extractor_model and judge_model strings."""
    try:
        from src.tui.widgets.model_bar import ModelBar
    except ImportError:
        pytest.xfail("ModelBar not yet created")

    msg = ModelBar.Changed("gpt-4o-mini", "claude-3-5-haiku-20241022")
    assert msg.extractor_model == "gpt-4o-mini"
    assert msg.judge_model == "claude-3-5-haiku-20241022"
