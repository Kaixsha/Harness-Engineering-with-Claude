import pytest

from src.agentic_loop import (
    END_TURN,
    TOOL_USE,
    run_agent,
    should_continue,
    should_terminate,
)


def test_tool_use_should_continue():
    assert should_continue(TOOL_USE) is True


def test_end_turn_should_not_continue():
    assert should_continue(END_TURN) is False


def test_end_turn_should_terminate():
    assert should_terminate(END_TURN) is True


def test_tool_use_should_not_terminate():
    assert should_terminate(TOOL_USE) is False


def test_agent_continues_after_tool_use():
    executed_tools = []

    def fake_tool_executor(tool_name, tool_input):
        executed_tools.append(
            {
                "tool": tool_name,
                "input": tool_input,
            }
        )

    responses = [
        {
            "stop_reason": "tool_use",
            "tool": "check_claim",
            "tool_input": {"claim_id": "CLM-1001"},
        },
        {
            "stop_reason": "end_turn",
            "result": "route",
        },
    ]

    output = run_agent(responses, fake_tool_executor)

    assert len(executed_tools) == 1
    assert executed_tools[0]["tool"] == "check_claim"
    assert output["status"] == "completed"
    assert output["result"] == "route"


def test_trace_records_stop_reasons():
    def fake_tool_executor(tool_name, tool_input):
        return None

    responses = [
        {
            "stop_reason": "tool_use",
            "tool": "check_claim",
            "tool_input": {"claim_id": "CLM-1001"},
        },
        {
            "stop_reason": "tool_use",
            "tool": "check_policy",
            "tool_input": {"claim_id": "CLM-1001"},
        },
        {
            "stop_reason": "end_turn",
            "result": "route",
        },
    ]

    output = run_agent(responses, fake_tool_executor)

    assert output["trace"] == [
        {"turn": 1, "stop_reason": "tool_use"},
        {"turn": 2, "stop_reason": "tool_use"},
        {"turn": 3, "stop_reason": "end_turn"},
    ]


def test_unknown_stop_reason_raises_error():
    responses = [
        {
            "stop_reason": "something_else",
        }
    ]

    with pytest.raises(ValueError):
        run_agent(responses, lambda tool_name, tool_input: None)


def test_missing_end_turn_raises_error():
    responses = [
        {
            "stop_reason": "tool_use",
            "tool": "check_claim",
            "tool_input": {},
        }
    ]

    with pytest.raises(RuntimeError):
        run_agent(responses, lambda tool_name, tool_input: None)
