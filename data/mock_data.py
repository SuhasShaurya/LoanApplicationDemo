from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel

class LoanApplicationData(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    loan_tenure_months: int
    existing_liabilities: float
    location: str
    application_timestamp: str

MOCK_LOAN_APPLICATIONS: List[Dict] = [
    {
        "applicant_id": "APP001",
        "age": 35,
        "income": 75000.0,
        "employment_type": "Full-time",
        "credit_score": 750,
        "loan_amount": 250000.0,
        "loan_tenure_months": 240,
        "existing_liabilities": 50000.0,
        "location": "New York",
        "application_timestamp": datetime.now().isoformat(),
    },
    {
        "applicant_id": "APP002",
        "age": 28,
        "income": 45000.0,
        "employment_type": "Contract",
        "credit_score": 580,
        "loan_amount": 150000.0,
        "loan_tenure_months": 180,
        "existing_liabilities": 80000.0,
        "location": "Los Angeles",
        "application_timestamp": datetime.now().isoformat(),
    },
    {
        "applicant_id": "APP003",
        "age": 45,
        "income": 120000.0,
        "employment_type": "Full-time",
        "credit_score": 780,
        "loan_amount": 400000.0,
        "loan_tenure_months": 300,
        "existing_liabilities": 100000.0,
        "location": "San Francisco",
        "application_timestamp": datetime.now().isoformat(),
    },
    {
        "applicant_id": "APP004",
        "age": 32,
        "income": 60000.0,
        "employment_type": "Part-time",
        "credit_score": 620,
        "loan_amount": 200000.0,
        "loan_tenure_months": 240,
        "existing_liabilities": 120000.0,
        "location": "Chicago",
        "application_timestamp": datetime.now().isoformat(),
    },
    {
        "applicant_id": "APP005",
        "age": 50,
        "income": 95000.0,
        "employment_type": "Self-employed",
        "credit_score": 700,
        "loan_amount": 300000.0,
        "loan_tenure_months": 240,
        "existing_liabilities": 75000.0,
        "location": "Boston",
        "application_timestamp": datetime.now().isoformat(),
    },
]

def get_mock_applicant(applicant_id: str) -> Dict:
    """Retrieve mock applicant data by ID"""
    for app in MOCK_LOAN_APPLICATIONS:
        if app["applicant_id"] == applicant_id:
            return app
    return None

def get_all_mock_applications() -> List[Dict]:
    """Return all mock loan applications"""
    return MOCK_LOAN_APPLICATIONS
