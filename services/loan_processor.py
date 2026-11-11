from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
try:
    from orchestration.orchestrator import create_orchestrator
except ImportError:
    from orchestration.simple_orchestrator import create_simple_orchestrator as create_orchestrator

class LoanApplicationRequest(BaseModel):
    """Full loan application with user input data"""
    applicant_id: str = Field(..., description="Unique identifier for the applicant")
    age: int = Field(..., ge=18, le=100, description="Age of applicant")
    income: float = Field(..., gt=0, description="Annual income in USD")
    employment_type: str = Field(..., description="Type of employment")
    credit_score: int = Field(..., ge=300, le=850, description="Credit score")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount in USD")
    loan_tenure_months: int = Field(..., ge=12, le=360, description="Loan tenure in months")
    existing_liabilities: float = Field(..., ge=0, description="Existing liabilities in USD")
    location: str = Field(..., description="Applicant's location")

class LoanApplicationResponse(BaseModel):
    application_id: str
    applicant_id: str
    decision: str
    risk_score: float
    confidence: float
    explanation: str
    case_id: str
    timestamp: str

async def process_loan_application(request: LoanApplicationRequest) -> Dict[str, Any]:
    """Process a loan application through the orchestration pipeline."""

    # Convert request to dict for orchestrator
    applicant_data = request.dict()

    orchestrator = create_orchestrator()

    # Check if orchestrator has async method
    import inspect
    if inspect.iscoroutinefunction(orchestrator.process_loan_application):
        result = await orchestrator.process_loan_application(applicant_data)
    else:
        # For simple orchestrator (sync version)
        result = orchestrator.process_loan_application(applicant_data)

    return result
