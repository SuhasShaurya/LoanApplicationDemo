from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from config.settings import settings
from services.loan_processor import process_loan_application, LoanApplicationRequest

app = FastAPI(
    title="Loan Approval System API",
    description="Multi-Agent Agentic AI Loan Approval System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    error: str
    applicant_id: str = None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Loan Approval System API is running"
    }

@app.get("/system-info")
async def get_system_info():
    """Get system information and capabilities."""
    return {
        "system": "Loan Approval System",
        "version": "1.0.0",
        "agents": 4,
        "mcp_servers": 4,
        "supported_decisions": ["Approve", "Reject", "Review"],
        "input_parameters": [
            "applicant_id",
            "age",
            "income",
            "employment_type",
            "credit_score",
            "loan_amount",
            "loan_tenure_months",
            "existing_liabilities",
            "location"
        ]
    }

@app.post("/apply-loan")
async def apply_for_loan(request: LoanApplicationRequest):
    """Submit a loan application for approval."""
    try:
        result = await process_loan_application(request)

        if "error" in result and result["error"] is not None:
            raise HTTPException(status_code=404, detail=result["error"])

        return {
            "application_id": result.get("application_id"),
            "applicant_id": result.get("applicant_id"),
            "decision": result.get("decision"),
            "risk_score": result.get("risk_score"),
            "confidence": result.get("confidence"),
            "explanation": result.get("explanation"),
            "case_id": result.get("case_id"),
            "timestamp": result.get("timestamp"),
            "profile_analysis": result.get("profile_analysis"),
            "risk_analysis": result.get("risk_analysis"),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing application: {str(e)}")

@app.get("/decision-history/{application_id}")
async def get_decision_history(application_id: str):
    """Retrieve decision history (placeholder for database integration)."""
    return {
        "application_id": application_id,
        "status": "Application decision cached",
        "message": "Database integration needed for persistent storage"
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT
    )
