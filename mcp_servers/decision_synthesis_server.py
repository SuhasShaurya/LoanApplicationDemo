from typing import Dict, Any

def synthesize_loan_decision(
    profile_analysis: dict,
    risk_analysis: dict,
    applicant_id: str
) -> dict:
    """Synthesize all analyses into a loan decision (Approve/Reject/Review)."""

    income_stability = profile_analysis.get("income_stability_score", 0)
    employment_risk = profile_analysis.get("employment_risk", "Unknown")
    dti_ratio = risk_analysis.get("debt_to_income_ratio", 1.0)
    credit_risk = risk_analysis.get("credit_score_risk_level", "Very High")
    loan_risk = risk_analysis.get("loan_amount_risk", "Very High")
    financial_risk_score = risk_analysis.get("overall_financial_risk_score", 1.0)
    anomalies = risk_analysis.get("anomalies_detected", [])

    decision, confidence, risk_score = make_decision(
        income_stability,
        employment_risk,
        dti_ratio,
        credit_risk,
        loan_risk,
        financial_risk_score,
        len(anomalies)
    )

    return {
        "applicant_id": applicant_id,
        "classification": decision,
        "risk_score": risk_score,
        "confidence_level": confidence,
        "key_decision_factors": get_decision_factors(
            income_stability, employment_risk, dti_ratio, credit_risk, loan_risk
        ),
        "explanation": generate_explanation(
            decision, income_stability, dti_ratio, credit_risk, employment_risk, anomalies
        ),
        "decision_reasoning": get_decision_reasoning(
            decision, income_stability, dti_ratio, credit_risk, loan_risk, employment_risk, financial_risk_score
        ),
    }

def make_decision(
    income_stability: float,
    employment_risk: str,
    dti: float,
    credit_risk: str,
    loan_risk: str,
    financial_risk: float,
    anomaly_count: int
) -> tuple:
    """Make loan decision based on weighted scoring of all factors."""

    # Convert categorical variables to numeric scores (0-1 scale)
    employment_score = _risk_to_score(employment_risk)
    credit_score = _risk_to_score(credit_risk)
    loan_score = _risk_to_score(loan_risk)

    # Normalize DTI (0.3 is good, 0.6+ is bad)
    dti_score = min(1.0, max(0.0, dti / 0.6))

    # Weighted scoring system
    # Weights: credit (35%), income stability (25%), DTI (25%), employment (10%), loan amount (5%)
    overall_score = (
        credit_score * 0.35 +
        (1 - income_stability) * 0.25 +  # Lower income stability = worse
        dti_score * 0.25 +
        employment_score * 0.10 +
        loan_score * 0.05
    )

    # Adjust for anomalies
    if anomaly_count > 0:
        overall_score = min(1.0, overall_score + (0.05 * anomaly_count))

    # Adjust for financial risk
    overall_score = min(1.0, overall_score * (1 + (financial_risk * 0.2)))

    # Decision thresholds - Only APPROVE or REJECT (no Review state)
    # Threshold at 0.45: Below = APPROVE, At or Above = REJECT
    if overall_score < 0.45:
        decision = "Approve"
        confidence = 0.88 + (0.45 - overall_score) * 0.1  # Higher confidence for better scores
        risk_score = 0.15 + overall_score * 0.3
    else:
        decision = "Reject"
        confidence = 0.80 + (overall_score - 0.45) * 0.2
        risk_score = 0.45 + (overall_score - 0.45) * 1.0

    return decision, confidence, risk_score

def _risk_to_score(risk_level: str) -> float:
    """Convert risk level string to numeric score (0-1)."""
    risk_map = {
        "Very Low": 0.1,
        "Low": 0.25,
        "Medium": 0.5,
        "High": 0.75,
        "Very High": 0.95,
        "Unknown": 0.5,
    }
    return risk_map.get(risk_level, 0.5)

def get_decision_factors(
    income_stability: float,
    employment_risk: str,
    dti: float,
    credit_risk: str,
    loan_risk: str
) -> list:
    """Identify key factors influencing the decision."""
    factors = []

    if income_stability >= 0.8:
        factors.append("Strong income stability")
    elif income_stability < 0.6:
        factors.append("Weak income stability")

    if employment_risk == "Low":
        factors.append("Stable employment")
    elif employment_risk == "High":
        factors.append("Unstable employment")

    if dti < 0.3:
        factors.append("Healthy debt-to-income ratio")
    elif dti > 0.5:
        factors.append("High debt-to-income ratio")

    if credit_risk in ["Very Low", "Low"]:
        factors.append("Good credit profile")
    elif credit_risk in ["High", "Very High"]:
        factors.append("Poor credit profile")

    if loan_risk == "Low":
        factors.append("Reasonable loan amount")
    elif loan_risk == "Very High":
        factors.append("Excessive loan amount")

    return factors if factors else ["Mixed financial profile"]

def generate_explanation(decision: str, income_stability: float, dti: float, credit_risk: str, employment_risk: str, anomalies: list) -> str:
    """Generate human-readable explanation for decision."""
    explanations = {
        "Approve": (
            f"Loan APPROVED - Applicant demonstrates strong financial capacity. "
            f"Income stability: {income_stability:.2f}/1.0, DTI: {dti:.2f}, Credit: {credit_risk}, Employment: {employment_risk}."
        ),
        "Reject": (
            f"Loan REJECTED - Applicant does not meet lending criteria. "
            f"Income stability: {income_stability:.2f}/1.0, DTI: {dti:.2f}, Credit: {credit_risk}, Employment: {employment_risk}."
        ),
        "Review": (
            f"REQUIRES MANUAL REVIEW - Mixed financial signals detected. "
            f"Income stability: {income_stability:.2f}/1.0, DTI: {dti:.2f}, Credit: {credit_risk}, Employment: {employment_risk}."
        ),
    }

    explanation = explanations.get(decision, "Unable to determine decision.")

    if anomalies:
        explanation += f" Flagged issues: {'; '.join(anomalies[:3])}"

    return explanation

def get_decision_reasoning(decision: str, income_stability: float, dti: float, credit_risk: str, loan_risk: str, employment_risk: str, financial_risk: float) -> dict:
    """Generate detailed reasoning for the decision."""
    return {
        "primary_factors": [
            f"Income Stability Score: {income_stability:.2f}",
            f"Debt-to-Income Ratio: {dti:.2f}",
            f"Credit Risk Level: {credit_risk}",
            f"Employment Risk: {employment_risk}",
            f"Loan Risk: {loan_risk}",
            f"Overall Financial Risk: {financial_risk:.2f}",
        ],
        "approval_criteria": get_approval_criteria(income_stability, dti, credit_risk, employment_risk, financial_risk),
        "decision_basis": f"Based on weighted analysis of credit profile ({credit_risk}), income stability ({income_stability:.2f}), and debt capacity (DTI: {dti:.2f})",
    }

def get_approval_criteria(income_stability: float, dti: float, credit_risk: str, employment_risk: str, financial_risk: float) -> dict:
    """Check specific approval criteria."""
    return {
        "meets_minimum_income_stability": income_stability >= 0.5,
        "acceptable_dti_ratio": dti <= 0.6,
        "credit_score_acceptable": credit_risk not in ["Very High"],
        "employment_stable": employment_risk != "High",
        "acceptable_financial_risk": financial_risk < 0.7,
    }

