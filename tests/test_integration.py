import pytest
from data.mock_data import get_mock_applicant, MOCK_LOAN_APPLICATIONS
from mcp_servers.applicant_db_server import get_applicant_profile
from mcp_servers.risk_rules_db_server import analyze_financial_risk
from mcp_servers.decision_synthesis_server import synthesize_loan_decision
from mcp_servers.notification_system_server import execute_loan_action
from orchestration.orchestrator import create_orchestrator
import asyncio

class TestMCPServers:
    """Test MCP Server Functions"""

    def test_applicant_db_server(self):
        """Test ApplicantDB MCP server."""
        applicant_id = MOCK_LOAN_APPLICATIONS[0]["applicant_id"]
        result = get_applicant_profile(applicant_id)

        assert result is not None
        assert "income_stability_score" in result
        assert "employment_risk" in result
        assert "credit_history_summary" in result
        assert result["income_stability_score"] >= 0 and result["income_stability_score"] <= 1

    def test_risk_rules_db_server(self):
        """Test RiskRulesDB MCP server."""
        applicant_id = MOCK_LOAN_APPLICATIONS[0]["applicant_id"]
        result = analyze_financial_risk(applicant_id)

        assert result is not None
        assert "debt_to_income_ratio" in result
        assert "credit_score_risk_level" in result
        assert "loan_amount_risk" in result
        assert "anomalies_detected" in result

    def test_decision_synthesis_server(self):
        """Test DecisionSynthesis MCP server."""
        profile_analysis = {
            "income_stability_score": 0.8,
            "employment_risk": "Low",
        }
        risk_analysis = {
            "debt_to_income_ratio": 0.3,
            "credit_score_risk_level": "Low",
            "loan_amount_risk": "Low",
            "overall_financial_risk_score": 0.2,
            "anomalies_detected": [],
        }

        result = synthesize_loan_decision(profile_analysis, risk_analysis, "APP001")

        assert result is not None
        assert "classification" in result
        assert result["classification"] in ["Approve", "Reject", "Review"]
        assert "risk_score" in result
        assert "confidence_level" in result

    def test_notification_system_server(self):
        """Test NotificationSystem MCP server."""
        result = execute_loan_action(
            applicant_id="APP001",
            decision="Approve",
            risk_score=0.2,
            confidence=0.95,
            explanation="Good financial profile"
        )

        assert result is not None
        assert "case_id" in result
        assert "action_taken" in result
        assert "notification_sent" in result
        assert "timestamp" in result

class TestAgents:
    """Test Individual Agents"""

    def test_applicant_profile_agent(self):
        """Test applicant profile agent."""
        from agents.applicant_profile_agent import run_applicant_profile_analysis

        applicant_id = MOCK_LOAN_APPLICATIONS[0]["applicant_id"]
        result = run_applicant_profile_analysis(applicant_id)

        assert result is not None
        assert "income_stability_score" in result

    def test_financial_risk_agent(self):
        """Test financial risk agent."""
        from agents.financial_risk_agent import run_financial_risk_analysis

        applicant_id = MOCK_LOAN_APPLICATIONS[0]["applicant_id"]
        result = run_financial_risk_analysis(applicant_id)

        assert result is not None
        assert "debt_to_income_ratio" in result

    def test_loan_decision_agent(self):
        """Test loan decision agent."""
        from agents.loan_decision_agent import run_loan_decision_analysis

        profile = {"income_stability_score": 0.8, "employment_risk": "Low"}
        risk = {
            "debt_to_income_ratio": 0.3,
            "credit_score_risk_level": "Low",
            "loan_amount_risk": "Low",
            "overall_financial_risk_score": 0.2,
            "anomalies_detected": [],
        }

        result = run_loan_decision_analysis(profile, risk, "APP001")

        assert result is not None
        assert "classification" in result

    def test_compliance_agent(self):
        """Test compliance agent."""
        from agents.compliance_agent import run_compliance_action

        result = run_compliance_action(
            applicant_id="APP001",
            decision="Approve",
            risk_score=0.2,
            confidence=0.95,
            explanation="Good financial profile"
        )

        assert result is not None
        assert "case_id" in result

class TestOrchestrator:
    """Test Orchestration Layer"""

    @pytest.mark.asyncio
    async def test_orchestrator_workflow(self):
        """Test the complete orchestration workflow."""
        orchestrator = create_orchestrator()
        applicant_data = MOCK_LOAN_APPLICATIONS[0]

        result = await orchestrator.process_loan_application(applicant_data)

        assert result is not None
        assert "application_id" in result
        assert "applicant_id" in result
        assert "decision" in result
        assert result["decision"] in ["Approve", "Reject", "Review"]
        assert "risk_score" in result
        assert "confidence" in result
        assert "case_id" in result

    @pytest.mark.asyncio
    async def test_orchestrator_multiple_applicants(self):
        """Test orchestrator with multiple applicants."""
        orchestrator = create_orchestrator()

        for applicant_data in MOCK_LOAN_APPLICATIONS[:3]:
            result = await orchestrator.process_loan_application(applicant_data)
            assert result["decision"] in ["Approve", "Reject", "Review"]
            print(f"Applicant {result['applicant_id']}: {result['decision']} (Case: {result['case_id']})")

class TestMockData:
    """Test Mock Data Retrieval"""

    def test_mock_data_availability(self):
        """Test that mock data is available."""
        assert len(MOCK_LOAN_APPLICATIONS) > 0

    def test_get_mock_applicant(self):
        """Test retrieval of mock applicant."""
        applicant_id = MOCK_LOAN_APPLICATIONS[0]["applicant_id"]
        applicant = get_mock_applicant(applicant_id)

        assert applicant is not None
        assert applicant["applicant_id"] == applicant_id

    def test_invalid_applicant_id(self):
        """Test handling of invalid applicant ID."""
        applicant = get_mock_applicant("INVALID123")
        assert applicant is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
