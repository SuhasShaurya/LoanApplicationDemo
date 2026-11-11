from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class LoanApplicationState:
    """State for loan application processing workflow."""

    application_id: str
    applicant_id: str
    applicant_data: Dict[str, Any]

    profile_analysis: Optional[Dict[str, Any]] = None
    risk_analysis: Optional[Dict[str, Any]] = None
    decision_result: Optional[Dict[str, Any]] = None
    action_result: Optional[Dict[str, Any]] = None

    final_decision: Optional[str] = None
    final_risk_score: Optional[float] = None
    final_confidence: Optional[float] = None
    final_explanation: Optional[str] = None

    case_id: Optional[str] = None
    timestamp: Optional[str] = None

    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            "application_id": self.application_id,
            "applicant_id": self.applicant_id,
            "applicant_data": self.applicant_data,
            "profile_analysis": self.profile_analysis,
            "risk_analysis": self.risk_analysis,
            "decision_result": self.decision_result,
            "action_result": self.action_result,
            "final_decision": self.final_decision,
            "final_risk_score": self.final_risk_score,
            "final_confidence": self.final_confidence,
            "final_explanation": self.final_explanation,
            "case_id": self.case_id,
            "timestamp": self.timestamp,
            "error": self.error,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "LoanApplicationState":
        """Create state from dictionary."""
        return LoanApplicationState(**data)
