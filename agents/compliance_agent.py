from typing import Dict, Any
from mcp_servers.notification_system_server import execute_loan_action

def run_compliance_action(
    applicant_data: Dict[str, Any],
    decision: str,
    risk_score: float,
    confidence: float,
    explanation: str
) -> Dict[str, Any]:
    """Run compliance agent to execute action and send notification."""
    applicant_id = applicant_data.get("applicant_id", "Unknown")
    action_result = execute_loan_action(applicant_id, decision, risk_score, confidence, explanation)
    return action_result
