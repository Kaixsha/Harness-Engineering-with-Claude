"""Run sample claims end-to-end and produce evidence artifacts."""

import json
from pathlib import Path

from src.agentic_loop import run_agent
from src.claims import route_claim


SAMPLE_CLAIMS = [
    {
        "claim_id": "CLM-2001",
        "amount": 1200,
        "category": "hardware",
    },
    {
        "claim_id": "CLM-2002",
        "amount": 7500,
        "category": "software",
    },
    {
        "claim_id": "CLM-2003",
        "amount": 300,
        "category": "network",
    },
    {
        "claim_id": "CLM-2004",
    },
]


def execute_tool(tool_name, tool_input):
    """Execute a supported claim tool."""
    if tool_name == "route_claim":
        return route_claim(tool_input)

    raise ValueError(f"Unknown tool: {tool_name}")


def build_responses(claim):
    """Build a deterministic demonstration of the agent loop."""
    decision = route_claim(claim)

    return [
        {
            "stop_reason": "tool_use",
            "tool": "route_claim",
            "tool_input": claim,
        },
        {
            "stop_reason": "end_turn",
            "result": decision["decision"],
        },
    ]


def process_claim(claim):
    """Process one claim through the stop_reason-driven loop."""
    responses = build_responses(claim)

    output = run_agent(
        responses=responses,
        tool_executor=execute_tool,
    )

    decision = route_claim(claim)

    return {
        "claim_id": decision["claim_id"],
        "decision": decision["decision"],
        "reason": decision["reason"],
        "trace": output["trace"],
    }


def run_claim_batch():
    """Process all sample claims."""
    return [process_claim(claim) for claim in SAMPLE_CLAIMS]


def write_artifact(results):
    """Write run evidence to the artifacts directory."""
    artifacts_directory = Path("artifacts")
    artifacts_directory.mkdir(exist_ok=True)

    artifact = {
        "run_id": "agentic-loop-run-001",
        "claims": results,
    }

    output_path = artifacts_directory / "run-001.json"

    output_path.write_text(
        json.dumps(artifact, indent=2),
        encoding="utf-8",
    )

    return output_path


def main():
    """Run the claim batch and save the artifact."""
    results = run_claim_batch()
    output_path = write_artifact(results)

    print(f"Artifact written to: {output_path}")

    for result in results:
        print(
            result["claim_id"],
            result["decision"],
            result["reason"],
        )


if __name__ == "__main__":
    main()
