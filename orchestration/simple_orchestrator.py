"""Simplified orchestrator that works without LangGraph (for testing)."""
import uuid
from datetime import datetime
from typing import Dict, Any
from orchestration.state import LoanApplicationState
from agents.applicant_profile_agent import run_applicant_profile_analysis
from agents.financial_risk_agent import run_financial_risk_analysis
from agents.loan_decision_agent import run_loan_decision_analysis
from agents.compliance_agent import run_compliance_action

class SimpleOrchestrator:
    """Simplified orchestrator for loan approval workflow."""

    def __init__(self):
        pass

    def process_loan_application(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a loan application through the workflow."""
        application_id = str(uuid.uuid4())[:8].upper()
        applicant_id = applicant_data.get("applicant_id")

        state = LoanApplicationState(
            application_id=application_id,
            applicant_id=applicant_id,
            applicant_data=applicant_data,
            timestamp=datetime.now().isoformat(),
        )

        try:
            # Step 1: Applicant Profile Analysis
            state.profile_analysis = run_applicant_profile_analysis(state.applicant_data)

            # Step 2: Financial Risk Analysis
            state.risk_analysis = run_financial_risk_analysis(state.applicant_data)

            # Step 3: Loan Decision
            decision_result = run_loan_decision_analysis(
                state.profile_analysis,
                state.risk_analysis,
                state.applicant_data
            )
            state.decision_result = decision_result
            state.final_decision = decision_result.get("classification")
            state.final_risk_score = decision_result.get("risk_score")
            state.final_confidence = decision_result.get("confidence_level")
            state.final_explanation = decision_result.get("explanation")

            # Step 4: Compliance and Action
            action_result = run_compliance_action(
                state.applicant_data,
                state.final_decision,
                state.final_risk_score,
                state.final_confidence,
                state.final_explanation
            )
            state.action_result = action_result
            state.case_id = action_result.get("case_id")

        except Exception as e:
            state.error = str(e)

        return {
            "application_id": state.application_id,
            "applicant_id": state.applicant_id,
            "decision": state.final_decision,
            "risk_score": state.final_risk_score,
            "confidence": state.final_confidence,
            "explanation": state.final_explanation,
            "case_id": state.case_id,
            "timestamp": state.timestamp,
            "profile_analysis": state.profile_analysis,
            "risk_analysis": state.risk_analysis,
            "error": state.error,
        }

def create_simple_orchestrator() -> SimpleOrchestrator:
    """Factory function to create simple orchestrator."""
    return SimpleOrchestrator()
