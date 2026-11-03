Agentic Loop System
This project implements a stop_reason-driven agentic loop with integrated tools.

Goals
Continue the agent loop when stop_reason is tool_use.
Execute requested tools and return their results to the model.
Terminate the loop when stop_reason is end_turn.
Process claims through routing or escalation.
Produce run and trace artifacts for verification.
Evidence
Evidence for this system will be stored in the artifacts directory.

Verification
The system will be verified using its automated pytest suite.
