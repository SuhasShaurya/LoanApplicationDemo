import uuid
from datetime import datetime
from typing import Dict, Any
from langgraph.graph import StateGraph
from orchestration.state import LoanApplicationState
from agents.applicant_profile_agent import run_applicant_profile_analysis
from agents.financial_risk_agent import run_financial_risk_analysis
from agents.loan_decision_agent import run_loan_decision_analysis
from agents.compliance_agent import run_compliance_action

class LoanOrchestrator:
    """Orchestrates the loan approval workflow using LangGraph."""

    def __init__(self):
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(LoanApplicationState)

        workflow.add_node("applicant_profile", self._applicant_profile_node)
        workflow.add_node("financial_risk", self._financial_risk_node)
        workflow.add_node("loan_decision", self._loan_decision_node)
        workflow.add_node("compliance_action", self._compliance_action_node)
        workflow.add_node("finalize", self._finalize_node)

        workflow.add_edge("applicant_profile", "financial_risk")
        workflow.add_edge("financial_risk", "loan_decision")
        workflow.add_edge("loan_decision", "compliance_action")
        workflow.add_edge("compliance_action", "finalize")

        workflow.set_entry_point("applicant_profile")

        return workflow.compile()

    def _applicant_profile_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute applicant profile analysis."""
        try:
            profile_analysis = run_applicant_profile_analysis(state.applicant_id)
            state.profile_analysis = profile_analysis
        except Exception as e:
            state.error = f"Applicant profile error: {str(e)}"
        return state

    def _financial_risk_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute financial risk analysis."""
        try:
            risk_analysis = run_financial_risk_analysis(state.applicant_id)
            state.risk_analysis = risk_analysis
        except Exception as e:
            state.error = f"Financial risk error: {str(e)}"
        return state

    def _loan_decision_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute loan decision synthesis."""
        try:
            decision_result = run_loan_decision_analysis(
                state.profile_analysis,
                state.risk_analysis,
                state.applicant_id
            )
            state.decision_result = decision_result
            state.final_decision = decision_result.get("classification")
            state.final_risk_score = decision_result.get("risk_score")
            state.final_confidence = decision_result.get("confidence_level")
            state.final_explanation = decision_result.get("explanation")
        except Exception as e:
            state.error = f"Loan decision error: {str(e)}"
        return state

    def _compliance_action_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute compliance and action orchestration."""
        try:
            action_result = run_compliance_action(
                state.applicant_id,
                state.final_decision,
                state.final_risk_score,
                state.final_confidence,
                state.final_explanation
            )
            state.action_result = action_result
            state.case_id = action_result.get("case_id")
        except Exception as e:
            state.error = f"Compliance action error: {str(e)}"
        return state

    def _finalize_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Finalize the workflow."""
        if not state.timestamp:
            state.timestamp = datetime.now().isoformat()
        return state

    async def process_loan_application(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a loan application through the workflow."""
        application_id = str(uuid.uuid4())[:8].upper()
        applicant_id = applicant_data.get("applicant_id")

        state = LoanApplicationState(
            application_id=application_id,
            applicant_id=applicant_id,
            applicant_data=applicant_data,
            timestamp=datetime.now().isoformat(),
        )

        result_state = self.workflow.invoke(state)

        return {
            "application_id": result_state.application_id,
            "applicant_id": result_state.applicant_id,
            "decision": result_state.final_decision,
            "risk_score": result_state.final_risk_score,
            "confidence": result_state.final_confidence,
            "explanation": result_state.final_explanation,
            "case_id": result_state.case_id,
            "timestamp": result_state.timestamp,
            "profile_analysis": result_state.profile_analysis,
            "risk_analysis": result_state.risk_analysis,
            "error": result_state.error,
        }

def create_orchestrator() -> LoanOrchestrator:
    """Factory function to create orchestrator."""
    return LoanOrchestrator()
