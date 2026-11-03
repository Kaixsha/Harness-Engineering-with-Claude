from src.claims import (
    ESCALATE,
    ROUTE,
    ESCALATION_THRESHOLD,
    is_complete,
    missing_fields,
    route_claim,
)


def test_complete_claim_is_complete():
    claim = {
        "claim_id": "CLM-1001",
        "amount": 1200,
        "category": "hardware",
    }

    assert is_complete(claim) is True


def test_missing_amount_is_incomplete():
    claim = {
        "claim_id": "CLM-1002",
        "category": "hardware",
    }

    assert is_complete(claim) is False


def test_missing_category_is_incomplete():
    claim = {
        "claim_id": "CLM-1003",
        "amount": 1000,
    }

    assert is_complete(claim) is False


def test_missing_fields_returns_expected_fields():
    claim = {
        "claim_id": "CLM-1004",
    }

    assert missing_fields(claim) == ["amount", "category"]


def test_standard_claim_routes():
    claim = {
        "claim_id": "CLM-1005",
        "amount": 1200,
        "category": "hardware",
    }

    result = route_claim(claim)

    assert result["decision"] == ROUTE
    assert result["reason"] == "eligible_for_standard_routing"


def test_claim_at_threshold_routes():
    claim = {
        "claim_id": "CLM-1006",
        "amount": ESCALATION_THRESHOLD,
        "category": "hardware",
    }

    result = route_claim(claim)

    assert result["decision"] == ROUTE


def test_claim_above_threshold_escalates():
    claim = {
        "claim_id": "CLM-1007",
        "amount": ESCALATION_THRESHOLD + 1,
        "category": "hardware",
    }

    result = route_claim(claim)

    assert result["decision"] == ESCALATE
    assert result["reason"] == "amount_above_threshold"


def test_missing_information_escalates():
    claim = {
        "claim_id": "CLM-1008",
    }

    result = route_claim(claim)

    assert result["decision"] == ESCALATE
    assert result["reason"] == "missing_required_information"


def test_negative_amount_escalates():
    claim = {
        "claim_id": "CLM-1009",
        "amount": -100,
        "category": "hardware",
    }

    result = route_claim(claim)

    assert result["decision"] == ESCALATE
    assert result["reason"] == "invalid_claim_amount"


def test_text_amount_escalates():
    claim = {
        "claim_id": "CLM-1010",
        "amount": "one thousand",
        "category": "hardware",
    }

    result = route_claim(claim)

    assert result["decision"] == ESCALATE
    assert result["reason"] == "invalid_claim_amount"


def test_zero_amount_routes():
    claim = {
        "claim_id": "CLM-1011",
        "amount": 0,
        "category": "hardware",
    }

    result = route_claim(claim)

    assert result["decision"] == ROUTE


def test_empty_category_escalates():
    claim = {
        "claim_id": "CLM-1012",
        "amount": 500,
        "category": "",
    }

    result = route_claim(claim)

    assert result["decision"] == ESCALATE


def test_every_valid_decision_is_route_or_escalate():
    claims = [
        {
            "claim_id": "CLM-1013",
            "amount": 250,
            "category": "hardware",
        },
        {
            "claim_id": "CLM-1014",
            "amount": 9000,
            "category": "software",
        },
        {
            "claim_id": "CLM-1015",
        },
    ]

    for claim in claims:
        result = route_claim(claim)

        assert result["decision"] in {ROUTE, ESCALATE}
