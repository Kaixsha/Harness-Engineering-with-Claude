from src.claims import ESCALATE, ROUTE
from src.run_claims import (
    SAMPLE_CLAIMS,
    build_responses,
    process_claim,
    run_claim_batch,
)


def test_sample_batch_contains_four_claims():
    assert len(SAMPLE_CLAIMS) == 4


def test_build_responses_starts_with_tool_use():
    responses = build_responses(SAMPLE_CLAIMS[0])

    assert responses[0]["stop_reason"] == "tool_use"


def test_build_responses_ends_with_end_turn():
    responses = build_responses(SAMPLE_CLAIMS[0])

    assert responses[-1]["stop_reason"] == "end_turn"


def test_processed_claim_contains_trace():
    result = process_claim(SAMPLE_CLAIMS[0])

    assert "trace" in result
    assert len(result["trace"]) == 2


def test_processed_claim_trace_starts_with_tool_use():
    result = process_claim(SAMPLE_CLAIMS[0])

    assert result["trace"][0]["stop_reason"] == "tool_use"


def test_processed_claim_trace_ends_with_end_turn():
    result = process_claim(SAMPLE_CLAIMS[0])

    assert result["trace"][-1]["stop_reason"] == "end_turn"


def test_standard_sample_claim_routes():
    result = process_claim(SAMPLE_CLAIMS[0])

    assert result["decision"] == ROUTE


def test_high_value_sample_claim_escalates():
    result = process_claim(SAMPLE_CLAIMS[1])

    assert result["decision"] == ESCALATE


def test_all_batch_claims_end_in_valid_decision():
    results = run_claim_batch()

    assert len(results) == len(SAMPLE_CLAIMS)

    for result in results:
        assert result["decision"] in {ROUTE, ESCALATE}
