from typing import Dict, Any
from mcp_servers.decision_synthesis_server import synthesize_loan_decision

def run_loan_decision_analysis(
    profile_analysis: Dict[str, Any],
    risk_analysis: Dict[str, Any],
    applicant_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Run loan decision agent to synthesize analysis and make decision."""
    applicant_id = applicant_data.get("applicant_id", "Unknown")
    decision_result = synthesize_loan_decision(profile_analysis, risk_analysis, applicant_id)
    return decision_result
