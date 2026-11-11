import uuid
from datetime import datetime
from typing import Dict, Any

def execute_loan_action(
    applicant_id: str,
    decision: str,
    risk_score: float,
    confidence: float,
    explanation: str
) -> dict:
    """Execute action and send notification based on loan decision."""

    case_id = str(uuid.uuid4())[:8].upper()
    timestamp = datetime.now().isoformat()

    action = get_action_for_decision(decision)
    notification = create_notification(applicant_id, decision, action, explanation)

    return {
        "action_taken": action,
        "notification_sent": notification,
        "case_id": case_id,
        "timestamp": timestamp,
        "summary": generate_action_summary(applicant_id, decision, case_id, action),
    }

def get_action_for_decision(decision: str) -> str:
    """Determine action based on decision."""
    actions = {
        "Approve": "Approve loan and proceed with fund disbursement",
        "Reject": "Reject loan application and notify applicant",
        "Review": "Forward to manual review team for further evaluation",
    }
    return actions.get(decision, "Unknown action")

def create_notification(applicant_id: str, decision: str, action: str, explanation: str) -> str:
    """Create notification message."""
    return f"Loan Application {applicant_id}: {decision}. Action: {action}. Details: {explanation}"

def generate_action_summary(applicant_id: str, decision: str, case_id: str, action: str) -> str:
    """Generate summary of actions taken."""
    return f"Case {case_id}: {decision} application for {applicant_id}. {action}"

