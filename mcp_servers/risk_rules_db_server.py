from typing import Dict, Any

def analyze_financial_risk(applicant_data: Dict[str, Any]) -> dict:
    """Analyze financial risk metrics for loan applicant."""
    if not applicant_data:
        return {"error": "Applicant data not provided"}

    applicant_id = applicant_data.get("applicant_id", "Unknown")
    income = applicant_data.get("income", 0)
    loan_amount = applicant_data.get("loan_amount", 0)
    existing_liabilities = applicant_data.get("existing_liabilities", 0)
    credit_score = applicant_data.get("credit_score", 0)
    loan_tenure_months = applicant_data.get("loan_tenure_months", 0)

    debt_to_income = calculate_debt_to_income(income, loan_amount, loan_tenure_months, existing_liabilities)
    credit_risk = classify_credit_risk(credit_score)
    loan_risk = classify_loan_risk(loan_amount, income)
    anomalies = detect_anomalies(applicant_data, debt_to_income, credit_score)

    return {
        "applicant_id": applicant_id,
        "debt_to_income_ratio": debt_to_income,
        "credit_score_risk_level": credit_risk,
        "loan_amount_risk": loan_risk,
        "anomalies_detected": anomalies,
        "reasoning": generate_risk_reasoning(debt_to_income, credit_risk, loan_risk, anomalies),
        "overall_financial_risk_score": calculate_overall_risk(debt_to_income, credit_risk, loan_risk),
    }

def calculate_debt_to_income(income: float, loan_amount: float, tenure_months: int, existing_liabilities: float) -> float:
    """Calculate debt-to-income ratio including monthly loan payment."""
    if income == 0:
        return 1.0
    monthly_income = income / 12
    monthly_loan_payment = loan_amount / tenure_months if tenure_months > 0 else loan_amount
    monthly_liabilities = existing_liabilities / 12
    total_monthly_debt = monthly_loan_payment + monthly_liabilities
    return total_monthly_debt / monthly_income

def classify_credit_risk(credit_score: int) -> str:
    """Classify credit risk based on credit score."""
    if credit_score >= 750:
        return "Very Low"
    elif credit_score >= 700:
        return "Low"
    elif credit_score >= 650:
        return "Medium"
    elif credit_score >= 600:
        return "High"
    else:
        return "Very High"

def classify_loan_risk(loan_amount: float, income: float) -> str:
    """Classify loan risk based on loan-to-income ratio."""
    if income == 0:
        return "Very High"
    loan_to_income = loan_amount / income
    if loan_to_income <= 2:
        return "Low"
    elif loan_to_income <= 3:
        return "Medium"
    elif loan_to_income <= 4:
        return "High"
    else:
        return "Very High"

def detect_anomalies(applicant: dict, dti: float, credit_score: int) -> list:
    """Detect anomalies in applicant data."""
    anomalies = []

    if dti > 0.5:
        anomalies.append("High debt-to-income ratio (>0.5)")

    if credit_score < 600:
        anomalies.append("Credit score below minimum threshold (600)")

    age = applicant.get("age", 0)
    if age < 21:
        anomalies.append("Applicant below minimum age")

    if age > 75:
        anomalies.append("Applicant near retirement age - repayment risk")

    employment_type = applicant.get("employment_type", "")
    if employment_type in ["Self-employed", "Contract", "Part-time"]:
        anomalies.append(f"Income stability concern: {employment_type} employment")

    return anomalies

def calculate_overall_risk(dti: float, credit_risk: str, loan_risk: str) -> float:
    """Calculate overall financial risk score (0-1, higher = more risky)."""
    risk_weights = {
        "Very Low": 0.1,
        "Low": 0.3,
        "Medium": 0.5,
        "High": 0.75,
        "Very High": 0.9,
    }

    credit_score = risk_weights.get(credit_risk, 0.5)
    loan_score = risk_weights.get(loan_risk, 0.5)
    dti_score = min(1.0, dti / 0.5)

    return (credit_score * 0.4 + loan_score * 0.3 + dti_score * 0.3)

def generate_risk_reasoning(dti: float, credit_risk: str, loan_risk: str, anomalies: list) -> str:
    """Generate human-readable risk analysis reasoning."""
    reasons = []
    reasons.append(f"Credit Risk: {credit_risk}")
    reasons.append(f"Loan Risk: {loan_risk}")
    reasons.append(f"DTI Ratio: {dti:.2f}")

    if anomalies:
        reasons.append(f"Anomalies: {', '.join(anomalies)}")

    return " | ".join(reasons)

