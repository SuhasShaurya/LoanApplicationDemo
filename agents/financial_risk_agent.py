from typing import Dict, Any
from mcp_servers.risk_rules_db_server import analyze_financial_risk

def run_financial_risk_analysis(applicant_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run financial risk agent to analyze financial metrics."""
    risk_analysis = analyze_financial_risk(applicant_data)
    return risk_analysis
