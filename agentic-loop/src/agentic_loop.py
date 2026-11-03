"""Agentic loop for processing claims using stop_reason."""

TOOL_USE = "tool_use"
END_TURN = "end_turn"


def should_continue(stop_reason):
    """Return True when the agent needs to continue using tools."""
    return stop_reason == TOOL_USE


def should_terminate(stop_reason):
    """Return True when the model has completed its turn."""
    return stop_reason == END_TURN
