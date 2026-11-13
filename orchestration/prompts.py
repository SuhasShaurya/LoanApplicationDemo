"""Prompt templates for LLM-based loan decision reasoning."""

# Chain-of-Thought Analysis Prompt
INITIAL_ANALYSIS_SYSTEM = """You are an expert loan approval analyst with 20 years of experience in financial assessment.
Your role is to provide detailed, thoughtful analysis of loan applications.
Think through all dimensions carefully and provide nuanced reasoning."""

INITIAL_ANALYSIS_USER = """Analyze this loan application with detailed reasoning using a structured approach.

## Applicant Profile
- Age: {age}
- Annual Income: ${income:,.0f}
- Employment Type: {employment_type}
- Employment Risk: {employment_risk}
- Income Stability Score: {income_stability:.2f}

## Financial Risk Analysis
- Debt-to-Income Ratio: {dti:.2f}
- Credit Score: {credit_score}
- Credit Risk Level: {credit_risk}
- Loan Amount: ${loan_amount:,.0f}
- Loan Risk Level: {loan_risk}
- Monthly Payment: ${monthly_payment:,.2f}

## Detected Anomalies
{anomalies}

## Analysis Framework

Please analyze this application through these six dimensions:

1. **Income Stability Assessment**
   - Evaluate the income stability score: {income_stability:.2f}
   - Assess employment type: {employment_type}
   - Consider employment risk level: {employment_risk}
   - Is income reliable and sustainable?

2. **Debt Capacity Analysis**
   - Current DTI ratio: {dti:.2f}
   - Industry benchmarks: Good <0.43, Acceptable <0.50, Concerning >0.50
   - Can this applicant comfortably handle the new loan payment?
   - What percentage of income goes to debt service?

3. **Credit Profile Evaluation**
   - Credit score: {credit_score}
   - Risk level: {credit_risk}
   - What payment history does this score suggest?
   - How reliable is this applicant historically?

4. **Loan Amount Reasonableness**
   - Loan-to-income ratio: {loan_to_income_ratio:.2f}
   - Industry benchmark: typically 2-3x is standard
   - Is this amount proportionate to the applicant's financial capacity?
   - Are there any red flags about loan sizing?

5. **Anomaly Impact**
   - Review detected anomalies: {anomalies}
   - How do these issues affect your assessment?
   - Can they be mitigated?

6. **Synthesis & Recommendation**
   - Synthesize all factors above
   - What is your overall assessment?
   - What drives your confidence or concern?
   - What is your recommended decision?

## Output Format

Provide your complete analysis as valid JSON with the following structure:
{{
  "income_analysis": "detailed analysis of income stability",
  "debt_analysis": "detailed analysis of debt capacity",
  "credit_analysis": "detailed analysis of credit profile",
  "loan_analysis": "detailed analysis of loan reasonableness",
  "anomaly_analysis": "impact of detected anomalies",
  "approval_likelihood": "High | Medium | Low",
  "key_positives": ["positive factor 1", "positive factor 2", ...],
  "key_risks": ["risk factor 1", "risk factor 2", ...],
  "recommended_decision": "Approve | Reject | Review",
  "confidence_level": <0-100>,
  "detailed_rationale": "comprehensive explanation of your recommendation"
}}

Think carefully through each dimension before providing your assessment."""

# Borderline Case Refinement Prompt
REFINEMENT_SYSTEM = """You are an expert loan review specialist reconsidering borderline applications.
Your role is to provide deeper analysis and consider factors that may have been underweighted initially.
Use fresh perspective while building on initial findings."""

REFINEMENT_USER = """This applicant scored borderline in initial review. Please provide deeper analysis for reconsideration.

## Initial Assessment
- Decision: {initial_decision}
- Confidence: {initial_confidence:.2%}
- Risk Score: {risk_score:.2f}
- Reason for Low Confidence: {low_confidence_reason}

## Applicant Strengths
{strengths}

## Applicant Concerns
{concerns}

## Detailed Reanalysis

Perform a deeper, more nuanced analysis considering:

1. **Potentially Underweighted Positive Factors**
   - What strengths might have been given insufficient weight?
   - Are there mitigating circumstances?
   - What positive signals do you see?

2. **Potentially Overweighted Concerns**
   - Which negative factors might be less critical than they appear?
   - Are there industry-standard explanations for these concerns?
   - Can risks be effectively managed?

3. **Market and Financial Context**
   - How do current economic conditions affect this assessment?
   - Are there relevant market trends?
   - How does this applicant compare to typical borrowers?

4. **Alternative Perspective**
   - Could this applicant succeed with this loan?
   - What would make you comfortable approving this?
   - What are the true decision drivers?

5. **Confidence Assessment**
   - Has your analysis revealed information that increases/decreases confidence?
   - Should the initial assessment be reconsidered?
   - What is your refined confidence level?

## Output Format

Provide your reanalysis as valid JSON:
{{
  "underweighted_positives": "analysis of underweighted strengths",
  "overweighted_concerns": "analysis of overweighted risks",
  "context_analysis": "market and financial context considerations",
  "refined_assessment": "your overall refined assessment",
  "refined_decision": "Approve | Reject | Review",
  "refined_confidence": <0-100>,
  "should_override_initial": true | false,
  "override_justification": "why the initial decision should or should not be overridden"
}}

Provide honest, thorough analysis without bias toward either approval or rejection."""

# Decision Explanation Prompt
EXPLANATION_SYSTEM = """You are a loan officer communicating decisions to applicants.
Your role is to provide clear, empathetic, professional explanations.
Be helpful while being honest about the decision."""

EXPLANATION_USER = """Create a clear, professional explanation of this loan decision for the applicant.

## Decision Details
- Decision: {decision}
- Confidence: {confidence:.2%}
- Risk Assessment: {risk_score:.2f}

## Key Factors Influencing Decision
{factors}

## Financial Metrics
- Income: ${income:,.0f}
- Debt-to-Income Ratio: {dti:.2f}
- Credit Score: {credit_score}
- Requested Loan: ${loan_amount:,.0f}

## Explanation Requirements

Create an explanation that:
1. States the decision clearly and directly
2. Explains major factors in plain language (avoid jargon)
3. Provides specific, actionable next steps
4. Includes relevant guidance or encouragement
5. Is professional but warm and approachable
6. Acknowledges positive aspects even if decision is rejection
7. Suggests improvements where applicable

## Constraints
- Keep total length under 200 words
- Use second person ("your") when appropriate
- Be specific (not vague)
- Provide hope or path forward

## Output

Provide just the explanation text (not in JSON). Make it something an applicant would appreciate receiving."""

# Confidence-Based Decision Prompt
CONFIDENCE_ASSESSMENT = """Assess your confidence in your recommendation on a scale of 0-100:

- 0-20: Very uncertain, many conflicting signals, significant unknowns
- 21-40: Uncertain, multiple concerning factors, recommend manual review
- 41-60: Moderate uncertainty, mixed signals, borderline case
- 61-80: Fairly confident, good supporting evidence, clear decision
- 81-100: Very confident, strong supporting evidence, clear and strong decision

Your confidence level should reflect:
1. Clarity of the decision (is it black-and-white or gray?)
2. Strength of supporting evidence
3. Presence of mitigating factors
4. Consistency across dimensions

What is your confidence level in your recommendation?"""

# Template for building complete analysis
COMPLETE_ANALYSIS_TEMPLATE = """Based on comprehensive analysis across six dimensions:

1. **Income Stability**: {income_analysis}
2. **Debt Capacity**: {debt_analysis}
3. **Credit Profile**: {credit_analysis}
4. **Loan Reasonableness**: {loan_analysis}
5. **Anomaly Assessment**: {anomaly_analysis}
6. **Overall Synthesis**: {synthesis}

**Recommendation**: {recommendation}
**Confidence**: {confidence}%

This analysis suggests a {likelihood} likelihood of approval."""


def format_initial_analysis_prompt(profile, risk, applicant_data):
    """Format initial analysis prompt with applicant data."""
    income = applicant_data.get('income', 0)
    loan_amount = applicant_data.get('loan_amount', 0)
    loan_tenure = applicant_data.get('loan_tenure_months', 12)

    monthly_payment = (loan_amount / loan_tenure * 12) if loan_tenure > 0 else 0
    loan_to_income = (loan_amount / income) if income > 0 else 0

    anomalies = risk.get('anomalies_detected', [])
    anomaly_text = "\n".join([f"  - {a}" for a in anomalies]) if anomalies else "  None detected"

    return INITIAL_ANALYSIS_USER.format(
        age=applicant_data.get('age', 0),
        income=income,
        employment_type=applicant_data.get('employment_type', 'Unknown'),
        employment_risk=profile.get('employment_risk', 'Unknown'),
        income_stability=profile.get('income_stability_score', 0.5),
        dti=risk.get('debt_to_income_ratio', 0.5),
        credit_score=applicant_data.get('credit_score', 0),
        credit_risk=risk.get('credit_score_risk_level', 'Unknown'),
        loan_amount=loan_amount,
        loan_risk=risk.get('loan_amount_risk', 'Unknown'),
        monthly_payment=monthly_payment,
        anomalies=anomaly_text,
        loan_to_income_ratio=loan_to_income
    )


def format_refinement_prompt(initial_analysis, applicant_data):
    """Format refinement prompt for borderline cases."""
    positives = initial_analysis.get('key_decision_factors', [])
    positives_text = "\n".join([f"  - {p}" for p in positives]) if positives else "  None identified"

    risks = initial_analysis.get('key_risks', [])
    if not risks:
        risks = []
        anomalies = initial_analysis.get('anomalies_detected', [])
        if anomalies:
            risks = anomalies
    risks_text = "\n".join([f"  - {r}" for r in risks]) if risks else "  None identified"

    return REFINEMENT_USER.format(
        initial_decision=initial_analysis.get('classification', 'Review'),
        initial_confidence=initial_analysis.get('confidence_level', 0.5) / 100.0,
        risk_score=initial_analysis.get('risk_score', 0.5),
        low_confidence_reason="Borderline metrics - mixed signals on approval viability",
        strengths=positives_text,
        concerns=risks_text
    )


def format_explanation_prompt(decision_result, applicant_data):
    """Format explanation prompt."""
    factors = decision_result.get('key_decision_factors', [])
    factors_text = "\n".join([f"  • {f}" for f in factors]) if factors else "  • Multiple financial factors considered"

    return EXPLANATION_USER.format(
        decision=decision_result.get('classification', 'Review'),
        confidence=decision_result.get('confidence_level', 0.5) / 100.0,
        risk_score=decision_result.get('risk_score', 0.5),
        factors=factors_text,
        income=applicant_data.get('income', 0),
        dti=decision_result.get('debt_to_income_ratio', 0.5),
        credit_score=applicant_data.get('credit_score', 0),
        loan_amount=applicant_data.get('loan_amount', 0)
    )
