"""Agentic loop for processing claims using stop_reason."""

TOOL_USE = "tool_use"
END_TURN = "end_turn"


def should_continue(stop_reason):
    """Return True when the agent needs to continue using tools."""
    return stop_reason == TOOL_USE


def should_terminate(stop_reason):
    """Return True when the model has completed its turn."""
    return stop_reason == END_TURN


def run_agent(responses, tool_executor):
    """Run the agent until the model returns end_turn."""
    trace = []

    for turn_number, response in enumerate(responses, start=1):
        stop_reason = response["stop_reason"]

        trace.append(
            {
                "turn": turn_number,
                "stop_reason": stop_reason,
            }
        )

        if should_continue(stop_reason):
            tool_name = response.get("tool")
            tool_input = response.get("tool_input", {})

            tool_executor(tool_name, tool_input)
            continue

        if should_terminate(stop_reason):
            return {
                "status": "completed",
                "result": response.get("result"),
                "trace": trace,
            }

        raise ValueError(
            f"Unsupported stop_reason: {stop_reason}"
        )

    raise RuntimeError(
        "Agent responses ended before end_turn was received."
    )
