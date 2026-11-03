"""Sample data used to evaluate the context strategy."""


CASE = {
    "case_id": "CASE-2048",
    "customer": "Northwind Retail",
    "product": "Cloud Inventory API",
    "severity": "high",
    "status": "investigating",
    "current_issue": "Inventory synchronization requests are timing out.",
}


HISTORY = [
    "Initial environment was provisioned successfully.",
    "Customer completed application onboarding.",
    "API authentication configuration was validated.",
    "Development testing completed without critical errors.",
    "Integration testing completed successfully.",
    "Customer migrated the first workload.",
    "Routine monitoring showed normal API latency.",
    "A maintenance activity was completed.",
    "Application configuration was reviewed.",
    "Database connection settings were validated.",
    "Customer reported intermittent synchronization latency.",
    "Support reproduced a synchronization timeout.",
]


EVENTS = [
    {
        "event_id": "EVT-001",
        "description": "Inventory synchronization timeout reproduced.",
        "relevant": True,
    },
    {
        "event_id": "EVT-002",
        "description": "Unrelated documentation review completed.",
        "relevant": False,
    },
    {
        "event_id": "EVT-003",
        "description": "API latency increased during synchronization.",
        "relevant": True,
    },
    {
        "event_id": "EVT-004",
        "description": "Routine account review completed.",
        "relevant": False,
    },
    {
        "event_id": "EVT-005",
        "description": "Timeout remains reproducible.",
        "relevant": True,
    },
]


RAW_NOTES = """
The case concerns Northwind Retail and the Cloud Inventory API.
The environment was originally provisioned successfully.
Application onboarding was completed.
Authentication was configured and validated.
Development testing completed without critical errors.
Integration testing completed successfully.
The customer migrated the first workload.
Routine monitoring initially showed normal API latency.
A maintenance activity was completed.
Application configuration was reviewed.
Database connection settings were validated.
Additional historical diagnostic notes were retained for reference.
Earlier monitoring data was retained for reference.
Previous support observations were retained for reference.
Older application events were retained for reference.
Older infrastructure events were retained for reference.
Older database observations were retained for reference.
Previous testing notes were retained for reference.
Previous onboarding notes were retained for reference.
Previous configuration notes were retained for reference.
Previous operational notes were retained for reference.
Historical troubleshooting details were retained for reference.
Historical monitoring details were retained for reference.
Historical customer observations were retained for reference.
The customer later reported intermittent synchronization latency.
Support reproduced a synchronization timeout.
API latency increased during synchronization.
The timeout remains reproducible.
The current case severity is high.
The current status is investigating.
The current issue is that inventory synchronization requests are timing out.
"""
