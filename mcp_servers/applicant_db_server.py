from typing import Any, Dict

def get_applicant_profile(applicant_data: Dict[str, Any]) -> dict:
    """Retrieve applicant profile and calculate stability metrics."""
    if not applicant_data:
        return {"error": "Applicant data not provided"}

    applicant_id = applicant_data.get("applicant_id", "Unknown")
    income = applicant_data.get("income", 0)
    age = applicant_data.get("age", 0)
    employment_type = applicant_data.get("employment_type", "Unknown")

    income_stability_score = calculate_income_stability(employment_type, age)
    employment_risk = classify_employment_risk(employment_type)
    credit_history_summary = f"Applicant {applicant_id} with ${income:,.0f}/year income, employed as {employment_type}"
    application_completeness = check_completeness(applicant_data)

    return {
        "applicant_id": applicant_id,
        "income_stability_score": income_stability_score,
        "employment_risk": employment_risk,
        "credit_history_summary": credit_history_summary,
        "application_completeness_flags": application_completeness,
        "age": age,
        "employment_type": employment_type,
        "annual_income": income,
    }

def calculate_income_stability(employment_type: str, age: int) -> float:
    """Calculate income stability score based on employment type and age."""
    stability_map = {
        "Full-time": 0.9,
        "Part-time": 0.6,
        "Self-employed": 0.5,
        "Contract": 0.4,
        "Retired": 0.7,
    }
    base_score = stability_map.get(employment_type, 0.5)
    age_bonus = 0.1 if age >= 35 else 0.0
    return min(1.0, base_score + age_bonus)

def classify_employment_risk(employment_type: str) -> str:
    """Classify employment risk level."""
    risk_map = {
        "Full-time": "Low",
        "Part-time": "Medium",
        "Self-employed": "High",
        "Contract": "High",
        "Retired": "Medium",
    }
    return risk_map.get(employment_type, "Unknown")

def check_completeness(applicant: dict) -> dict:
    """Check if all required fields are present in application."""
    required_fields = [
        "applicant_id", "age", "income", "employment_type",
        "credit_score", "loan_amount", "loan_tenure_months",
        "existing_liabilities", "location"
    ]
    missing = [field for field in required_fields if field not in applicant or applicant[field] is None]
    return {
        "all_fields_present": len(missing) == 0,
        "missing_fields": missing,
        "completeness_score": (len(required_fields) - len(missing)) / len(required_fields),
    }
