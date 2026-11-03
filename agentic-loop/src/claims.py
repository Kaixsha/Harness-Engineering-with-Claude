"""Claim validation and routing logic."""

ROUTE = "route"
ESCALATE = "escalate"

REQUIRED_FIELDS = (
    "claim_id",
    "amount",
    "category",
)

ESCALATION_THRESHOLD = 5000


def missing_fields(claim):
    """Return required claim fields that are missing or empty."""
    return [
        field
        for field in REQUIRED_FIELDS
        if field not in claim or claim[field] in (None, "")
    ]


def is_complete(claim):
    """Return True when all required claim fields are present."""
    return len(missing_fields(claim)) == 0


def route_claim(claim):
    """Return a deterministic routing decision for a claim."""

    missing = missing_fields(claim)

    if missing:
        return {
            "claim_id": claim.get("claim_id", "unknown"),
            "decision": ESCALATE,
            "reason": "missing_required_information",
            "missing_fields": missing,
        }

    amount = claim["amount"]

    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        return {
            "claim_id": claim["claim_id"],
            "decision": ESCALATE,
            "reason": "invalid_claim_amount",
        }

    if amount < 0:
        return {
            "claim_id": claim["claim_id"],
            "decision": ESCALATE,
            "reason": "invalid_claim_amount",
        }

    if amount > ESCALATION_THRESHOLD:
        return {
            "claim_id": claim["claim_id"],
            "decision": ESCALATE,
            "reason": "amount_above_threshold",
        }

    return {
        "claim_id": claim["claim_id"],
        "decision": ROUTE,
        "reason": "eligible_for_standard_routing",
    }
