"""Enhanced LangGraph orchestrator with conditional routing, error handling, and retries."""
import uuid
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from functools import wraps
from langgraph.graph import StateGraph, END
from orchestration.state import LoanApplicationState
from agents.applicant_profile_agent import run_applicant_profile_analysis
from agents.financial_risk_agent import run_financial_risk_analysis
from agents.loan_decision_agent import run_loan_decision_analysis
from agents.compliance_agent import run_compliance_action
from config.settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class EnhancedLoanOrchestrator:
    """Enhanced orchestrator with conditional routing, error handling, and retry logic."""

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize orchestrator with retry configuration.

        Args:
            max_retries: Maximum number of retries for failed nodes
            retry_delay: Delay between retries in seconds
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.workflow = self._build_workflow()
        self.execution_trace = []

    def _build_workflow(self) -> StateGraph:
        """Build the enhanced LangGraph workflow with conditional routing and error handling."""
        workflow = StateGraph(LoanApplicationState)

        # Add nodes for each stage
        workflow.add_node("applicant_profile", self._node_applicant_profile)
        workflow.add_node("financial_risk", self._node_financial_risk)
        workflow.add_node("loan_decision", self._node_loan_decision)
        workflow.add_node("route_decision", self._node_route_decision)
        workflow.add_node("compliance_action", self._node_compliance_action)
        workflow.add_node("manual_review", self._node_manual_review)
        workflow.add_node("error_handler", self._node_error_handler)
        workflow.add_node("finalize", self._node_finalize)

        # Set entry point
        workflow.set_entry_point("applicant_profile")

        # Add edges for sequential processing
        workflow.add_edge("applicant_profile", "financial_risk")
        workflow.add_edge("financial_risk", "loan_decision")
        workflow.add_edge("loan_decision", "route_decision")

        # Conditional edges based on confidence and risk
        workflow.add_conditional_edges(
            "route_decision",
            self._route_based_on_confidence,
            {
                "proceed": "compliance_action",
                "manual_review": "manual_review",
                "error": "error_handler"            }
        )

        # Continue from compliance and manual review to finalize
        workflow.add_edge("compliance_action", "finalize")
        workflow.add_edge("manual_review", "finalize")
        workflow.add_edge("error_handler", "finalize")

        # End point
        workflow.add_edge("finalize", END)

        return workflow.compile()

    def _retry_node(self, node_name: str, node_func):
        """Decorator to add retry logic to node functions.

        Args:
            node_name: Name of the node for logging
            node_func: The node function to execute

        Returns:
            Wrapper function with retry logic
        """
        @wraps(node_func)
        def wrapper(state: LoanApplicationState) -> LoanApplicationState:
            """Execute node with retry logic."""
            last_error = None

            for attempt in range(self.max_retries):
                try:
                    logger.info(f"[{node_name}] Execution attempt {attempt + 1}/{self.max_retries}")
                    result = node_func(state)
                    logger.info(f"[{node_name}] ✓ Success on attempt {attempt + 1}")
                    self._log_execution(node_name, "success", attempt)
                    return result
                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"[{node_name}] ✗ Attempt {attempt + 1} failed: {str(e)}"
                    )
                    if attempt < self.max_retries - 1:
                        asyncio.run(asyncio.sleep(self.retry_delay))

            # All retries exhausted
            logger.error(f"[{node_name}] ✗ All {self.max_retries} attempts failed")
            state.error = f"{node_name} failed after {self.max_retries} retries: {str(last_error)}"
            self._log_execution(node_name, "failed", self.max_retries)
            return state

        return wrapper

    def _log_execution(self, node_name: str, status: str, attempt: int):
        """Log node execution for tracing."""
        trace_entry = {
            "timestamp": datetime.now().isoformat(),
            "node": node_name,
            "status": status,
            "attempt": attempt
        }
        self.execution_trace.append(trace_entry)

    def _node_applicant_profile(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute applicant profile analysis with retry logic."""

        @self._retry_node("applicant_profile", lambda s: s)
        def execute(s):
            logger.info(f"[applicant_profile] Analyzing applicant {state.applicant_id}")
            profile_analysis = run_applicant_profile_analysis(state.applicant_data)
            s.profile_analysis = profile_analysis
            logger.info(
                f"[applicant_profile] ✓ Income Stability: "
                f"{profile_analysis.get('income_stability_score', 'N/A')}, "
                f"Employment Risk: {profile_analysis.get('employment_risk', 'N/A')}"
            )
            return s

        return execute(state)

    def _node_financial_risk(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute financial risk analysis with retry logic."""

        @self._retry_node("financial_risk", lambda s: s)
        def execute(s):
            logger.info(f"[financial_risk] Analyzing financial risk for {state.applicant_id}")
            risk_analysis = run_financial_risk_analysis(state.applicant_data)
            s.risk_analysis = risk_analysis
            logger.info(
                f"[financial_risk] ✓ DTI: {risk_analysis.get('debt_to_income_ratio', 'N/A'):.2f}, "
                f"Credit Risk: {risk_analysis.get('credit_score_risk_level', 'N/A')}"
            )
            return s

        return execute(state)

    def _node_loan_decision(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute loan decision synthesis with retry logic."""

        @self._retry_node("loan_decision", lambda s: s)
        def execute(s):
            logger.info(f"[loan_decision] Synthesizing decision for {state.applicant_id}")
            decision_result = run_loan_decision_analysis(
                state.profile_analysis,
                state.risk_analysis,
                state.applicant_data
            )
            s.decision_result = decision_result
            s.final_decision = decision_result.get("classification")
            s.final_risk_score = decision_result.get("risk_score")
            s.final_confidence = decision_result.get("confidence_level")
            s.final_explanation = decision_result.get("explanation")

            logger.info(
                f"[loan_decision] ✓ Decision: {s.final_decision}, "
                f"Confidence: {s.final_confidence:.2%}, Risk Score: {s.final_risk_score:.2f}"
            )
            return s

        return execute(state)

    def _route_based_on_confidence(self, state: LoanApplicationState) -> str:
        """Route based on confidence level and risk.

        Returns:
            "proceed" - Route to compliance for low-risk approvals
            "manual_review" - Route for borderline cases (low confidence)
            "error" - Route if there was an error
        """
        if state.error:
            logger.warning(f"[router] Error detected: {state.error}")
            return "error"

        confidence_threshold = getattr(
            settings,
            'MIN_CONFIDENCE_THRESHOLD',
            0.6
        )

        logger.info(
            f"[router] Routing decision - Confidence: {state.final_confidence:.2%}, "
            f"Threshold: {confidence_threshold:.2%}"
        )

        if state.final_confidence >= confidence_threshold:
            logger.info(f"[router] → Proceeding to compliance (high confidence)")
            return "proceed"
        else:
            logger.warning(
                f"[router] → Manual review required (low confidence: {state.final_confidence:.2%})"
            )
            state.requires_manual_review = True
            return "manual_review"

    def _node_route_decision(self, state: LoanApplicationState) -> LoanApplicationState:
        """Routing node - placeholder for branching logic."""
        logger.info(f"[routing] Making routing decision for {state.applicant_id}")
        return state

    def _node_compliance_action(self, state: LoanApplicationState) -> LoanApplicationState:
        """Execute compliance and action orchestration with retry logic."""

        @self._retry_node("compliance_action", lambda s: s)
        def execute(s):
            logger.info(f"[compliance_action] Executing compliance checks for {state.applicant_id}")
            action_result = run_compliance_action(
                state.applicant_data,
                state.final_decision,
                state.final_risk_score,
                state.final_confidence,
                state.final_explanation
            )
            s.action_result = action_result
            s.case_id = action_result.get("case_id")
            logger.info(f"[compliance_action] ✓ Case ID: {s.case_id}")
            return s

        return execute(state)

    def _node_manual_review(self, state: LoanApplicationState) -> LoanApplicationState:
        """Handle manual review flag for borderline cases."""
        logger.info(
            f"[manual_review] Flagging {state.applicant_id} for manual review "
            f"(confidence: {state.final_confidence:.2%})"
        )

        # Generate case ID for manual review
        case_id = f"MANUAL-{str(uuid.uuid4())[:12].upper()}"
        state.case_id = case_id
        state.requires_manual_review = True

        logger.info(f"[manual_review] ✓ Manual review case: {case_id}")
        return state

    def _node_error_handler(self, state: LoanApplicationState) -> LoanApplicationState:
        """Handle errors that occurred during processing."""
        logger.error(f"[error_handler] Processing error for {state.applicant_id}: {state.error}")

        # Fallback: Mark as requiring manual review
        if not state.case_id:
            case_id = f"ERROR-{str(uuid.uuid4())[:12].upper()}"
            state.case_id = case_id

        # Ensure decision is set
        if not state.final_decision:
            state.final_decision = "Review"

        logger.info(f"[error_handler] ✓ Error case: {state.case_id}")
        return state

    def _node_finalize(self, state: LoanApplicationState) -> LoanApplicationState:
        """Finalize the workflow and prepare output."""
        if not state.timestamp:
            state.timestamp = datetime.now().isoformat()

        logger.info(
            f"[finalize] Completed processing for {state.applicant_id} "
            f"(Case: {state.case_id}, Decision: {state.final_decision})"
        )
        return state

    async def process_loan_application(
        self,
        applicant_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a loan application through the enhanced workflow.

        Args:
            applicant_data: Applicant information

        Returns:
            Dictionary with decision and analysis results
        """
        application_id = str(uuid.uuid4())[:8].upper()
        applicant_id = applicant_data.get("applicant_id")

        logger.info(
            f"[orchestrator] Starting processing - Application: {application_id}, "
            f"Applicant: {applicant_id}"
        )

        # Initialize state
        state = LoanApplicationState(
            application_id=application_id,
            applicant_id=applicant_id,
            applicant_data=applicant_data,
            timestamp=datetime.now().isoformat(),
        )

        # Execute workflow
        result_state = self.workflow.invoke(state)

        # Prepare response - handle both dict and state object returns
        if isinstance(result_state, dict):
            # Dict from workflow.invoke - transform keys for consistent API
            response = {
                "application_id": result_state.get("application_id"),
                "applicant_id": result_state.get("applicant_id"),
                "decision": result_state.get("final_decision"),  # Map final_decision to decision
                "risk_score": result_state.get("final_risk_score"),
                "confidence": result_state.get("final_confidence"),
                "explanation": result_state.get("final_explanation"),
                "case_id": result_state.get("case_id"),
                "timestamp": result_state.get("timestamp"),
                "profile_analysis": result_state.get("profile_analysis"),
                "risk_analysis": result_state.get("risk_analysis"),
                "error": result_state.get("error"),
                "requires_manual_review": result_state.get("requires_manual_review", False),
            }
        else:
            # State object - transform to dict
            response = {
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
                "requires_manual_review": getattr(result_state, 'requires_manual_review', False),
            }

        logger.info(f"[orchestrator] Completed - Application: {application_id}")
        return response

    def get_execution_trace(self) -> list:
        """Get the execution trace for debugging and monitoring."""
        return self.execution_trace

    def clear_execution_trace(self):
        """Clear the execution trace."""
        self.execution_trace = []

    def get_workflow_graph(self) -> Dict[str, Any]:
        """Get workflow structure for visualization."""
        return {
            "nodes": [
                "applicant_profile",
                "financial_risk",
                "loan_decision",
                "route_decision",
                "compliance_action",
                "manual_review",
                "error_handler",
                "finalize"
            ],
            "edges": [
                ("applicant_profile", "financial_risk"),
                ("financial_risk", "loan_decision"),
                ("loan_decision", "route_decision"),
                ("route_decision", "compliance_action"),
                ("route_decision", "manual_review"),
                ("route_decision", "error_handler"),
                ("compliance_action", "finalize"),
                ("manual_review", "finalize"),
                ("error_handler", "finalize"),
                ("finalize", "END")
            ]
        }


def create_enhanced_orchestrator(
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> EnhancedLoanOrchestrator:
    """Factory function to create enhanced orchestrator.

    Args:
        max_retries: Maximum number of retries for failed nodes
        retry_delay: Delay between retries in seconds

    Returns:
        EnhancedLoanOrchestrator instance
    """
    return EnhancedLoanOrchestrator(max_retries=max_retries, retry_delay=retry_delay)
