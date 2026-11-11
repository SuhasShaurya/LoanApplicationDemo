from typing import Dict, Any
from mcp_servers.applicant_db_server import get_applicant_profile

def run_applicant_profile_analysis(applicant_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run applicant profile agent to analyze applicant details."""
    profile_analysis = get_applicant_profile(applicant_data)
    return profile_analysis
