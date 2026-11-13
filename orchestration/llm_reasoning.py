"""LLM-powered reasoning engine for loan decision analysis using Claude API."""
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from anthropic import Anthropic
from config.settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class LLMReasoningEngine:
    """LLM-powered reasoning engine for loan decision analysis."""

    def __init__(self):
        """Initialize LLM reasoning engine with Anthropic client."""
        self.client = Anthropic()
        self.model = getattr(settings, 'LLM_MODEL', 'claude-opus-4-1')
        self.temperature = getattr(settings, 'LLM_TEMPERATURE', 0.7)
        self.max_tokens = getattr(settings, 'LLM_MAX_TOKENS', 2000)
        logger.info(f"[LLMReasoningEngine] Initialized with model: {self.model}")

    async def analyze_decision(
        self,
        profile_analysis: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        applicant_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use Claude to analyze and reason about loan decision.

        Args:
            profile_analysis: Applicant profile analysis
            risk_analysis: Financial risk analysis
            applicant_data: Original applicant data

        Returns:
            Dictionary with LLM analysis results
        """
        try:
            logger.info(f"[llm_analysis] Starting LLM analysis for {applicant_data.get('applicant_id')}")

            prompt = self._build_initial_analysis_prompt(profile_analysis, risk_analysis, applicant_data)

            # Call Claude with extended thinking for better reasoning
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 5000
                },
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse response
            analysis = self._parse_analysis_response(response)
            logger.info(f"[llm_analysis] Analysis complete - Decision: {analysis['decision']}, "
                       f"Confidence: {analysis['confidence']:.2%}")

            return analysis

        except Exception as e:
            logger.error(f"[llm_analysis] Failed: {str(e)}")
            # Return empty analysis on failure - will fall back to rule-based
            return self._get_fallback_analysis()

    async def refine_borderline_decision(
        self,
        initial_analysis: Dict[str, Any],
        applicant_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Refine borderline decisions using LLM reasoning.

        Args:
            initial_analysis: Initial decision analysis result
            applicant_data: Original applicant data

        Returns:
            Dictionary with refined decision
        """
        try:
            logger.info(f"[refinement] Starting refinement for {applicant_data.get('applicant_id')} "
                       f"(confidence: {initial_analysis.get('confidence', 0):.2%})")

            prompt = self._build_refinement_prompt(initial_analysis, applicant_data)

            # Use extended thinking for borderline cases
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 8000  # More thinking for refinement
                },
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            refined = self._parse_refinement_response(response)
            logger.info(f"[refinement] Refinement complete - New Decision: {refined['decision']}, "
                       f"New Confidence: {refined['confidence']:.2%}")

            return refined

        except Exception as e:
            logger.error(f"[refinement] Failed: {str(e)}")
            # Return no refinement on failure - use original decision
            return {"decision": None, "confidence": None, "should_override": False}

    async def generate_explanation(
        self,
        decision_result: Dict[str, Any],
        applicant_data: Dict[str, Any]
    ) -> str:
        """Generate human-friendly explanation of the decision.

        Args:
            decision_result: Final decision result
            applicant_data: Original applicant data

        Returns:
            Human-friendly explanation string
        """
        try:
            prompt = self._build_explanation_prompt(decision_result, applicant_data)

            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=500,
                temperature=0.5,  # Lower temperature for consistency
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            explanation = response.content[0].text
            logger.info(f"[explanation] Generated explanation for {applicant_data.get('applicant_id')}")
            return explanation

        except Exception as e:
            logger.error(f"[explanation] Failed: {str(e)}")
            return "Unable to generate detailed explanation at this time."

    def _build_initial_analysis_prompt(
        self,
        profile: Dict[str, Any],
        risk: Dict[str, Any],
        applicant_data: Dict[str, Any]
    ) -> str:
        """Build chain-of-thought analysis prompt."""

        income_stability = profile.get('income_stability_score', 0.5)
        employment_risk = profile.get('employment_risk', 'Unknown')
        dti = risk.get('debt_to_income_ratio', 0.5)
        credit_risk = risk.get('credit_score_risk_level', 'Unknown')
        loan_risk = risk.get('loan_amount_risk', 'Unknown')
        anomalies = risk.get('anomalies_detected', [])
        income = applicant_data.get('income', 0)
        age = applicant_data.get('age', 0)
        credit_score = applicant_data.get('credit_score', 0)
        loan_amount = applicant_data.get('loan_amount', 0)
        employment_type = applicant_data.get('employment_type', 'Unknown')
        loan_tenure = applicant_data.get('loan_tenure_months', 0)

        monthly_payment = (loan_amount / loan_tenure * 12) if loan_tenure > 0 else 0
        loan_to_income = (loan_amount / income) if income > 0 else 0

        anomaly_text = "\n".join([f"  - {a}" for a in anomalies]) if anomalies else "  None detected"

        prompt = f"""You are an expert loan approval analyst. Analyze this loan application with detailed reasoning.

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
- Loan Tenure: {loan_tenure} months
- Monthly Payment: ${monthly_payment:,.2f}
- Loan-to-Income Ratio: {loan_to_income:.2f}

## Detected Anomalies
{anomaly_text}

## Your Analysis Task

Provide a comprehensive chain-of-thought analysis using JSON format:

1. **Income Stability Assessment**: Evaluate the income_stability_score ({income_stability:.2f}), employment type ({employment_type}), and employment risk ({employment_risk}).

2. **Debt Capacity Analysis**: Analyze DTI ratio ({dti:.2f}) against industry benchmarks (good: <0.43, acceptable: <0.50). Can applicant handle this loan?

3. **Credit Profile Evaluation**: Assess credit score ({credit_score}) and credit risk level ({credit_risk}). What payment behavior does this suggest?

4. **Loan Amount Reasonableness**: Evaluate loan-to-income ratio ({loan_to_income:.2f}) against industry benchmarks (standard: 2-3). Is this reasonable?

5. **Anomaly Impact**: Analyze detected anomalies and their impact on the decision.

6. **Overall Assessment**: Synthesize all factors and provide:
   - approval_likelihood: "High" | "Medium" | "Low"
   - key_positives: [list of positive factors]
   - key_risks: [list of risk factors]
   - recommended_decision: "Approve" | "Reject" | "Review"
   - confidence_level: 0-100 (numeric)
   - detailed_rationale: explanation of your recommendation

Return response as valid JSON with these exact fields:
{{
  "income_analysis": "...",
  "debt_analysis": "...",
  "credit_analysis": "...",
  "loan_analysis": "...",
  "anomaly_analysis": "...",
  "approval_likelihood": "High|Medium|Low",
  "key_positives": [...],
  "key_risks": [...],
  "recommended_decision": "Approve|Reject|Review",
  "confidence_level": <0-100>,
  "detailed_rationale": "..."
}}"""

        return prompt

    def _build_refinement_prompt(
        self,
        initial_analysis: Dict[str, Any],
        applicant_data: Dict[str, Any]
    ) -> str:
        """Build refinement prompt for borderline cases."""

        decision = initial_analysis.get('classification', 'Unknown')
        confidence = initial_analysis.get('confidence_level', 0)
        risk_score = initial_analysis.get('risk_score', 0)

        profile = initial_analysis.get('profile_analysis', {})
        risk = initial_analysis.get('risk_analysis', {})

        prompt = f"""You are reviewing a borderline loan application for reconsideration.

## Initial Assessment
- Decision: {decision}
- Confidence: {confidence:.2%}
- Risk Score: {risk_score:.2f}

## Applicant Strengths
{self._extract_strengths(initial_analysis)}

## Applicant Concerns
{self._extract_concerns(initial_analysis)}

## Refinement Analysis Task

Perform a deeper analysis for this borderline case:

1. **Underweighted Factors**: What positive factors might have been underweighted in the initial analysis?

2. **Overweighted Factors**: Are any negative factors being over-emphasized?

3. **Context Considerations**: What market or financial context should influence this decision?

4. **Refined Assessment**: Based on deeper analysis, should the decision be reconsidered?

5. **Final Recommendation**:
   - Refined decision: "Approve" | "Reject" | "Review"
   - Refined confidence: 0-100
   - Should this override the initial decision?
   - Why?

Return as JSON:
{{
  "underweighted_positives": "...",
  "overweighted_concerns": "...",
  "context_analysis": "...",
  "refined_assessment": "...",
  "refined_decision": "Approve|Reject|Review",
  "refined_confidence": <0-100>,
  "should_override": true|false,
  "override_justification": "..."
}}"""

        return prompt

    def _build_explanation_prompt(
        self,
        decision_result: Dict[str, Any],
        applicant_data: Dict[str, Any]
    ) -> str:
        """Build prompt for decision explanation."""

        decision = decision_result.get('classification', 'Review')
        confidence = decision_result.get('confidence_level', 0)
        risk_score = decision_result.get('risk_score', 0)
        factors = decision_result.get('key_decision_factors', [])

        factors_text = "\n".join([f"- {f}" for f in factors])

        prompt = f"""Generate a clear, professional explanation of this loan decision for the applicant:

Decision: {decision}
Confidence: {confidence:.2%}
Risk Score: {risk_score:.2f}

Key Factors:
{factors_text}

Create an empathetic, clear explanation that:
1. States the decision clearly
2. Explains the main factors (in layman's terms)
3. Provides specific next steps
4. Includes relevant guidance

Keep it under 150 words. Be professional but approachable."""

        return prompt

    def _parse_analysis_response(self, response) -> Dict[str, Any]:
        """Parse Claude response for analysis."""

        try:
            # Extract text content
            content = response.content[0].text

            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                analysis = json.loads(content)

            return {
                "analysis": analysis,
                "confidence": analysis.get('confidence_level', 50) / 100.0,  # Convert to 0-1
                "decision": analysis.get('recommended_decision', 'Review'),
                "reasoning": analysis.get('detailed_rationale', ''),
                "thinking": getattr(response, 'thinking', None)
            }

        except Exception as e:
            logger.error(f"[parse_analysis] Failed to parse response: {str(e)}")
            return self._get_fallback_analysis()

    def _parse_refinement_response(self, response) -> Dict[str, Any]:
        """Parse refinement response."""

        try:
            content = response.content[0].text

            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                refined = json.loads(json_match.group())
            else:
                refined = json.loads(content)

            return {
                "decision": refined.get('refined_decision'),
                "confidence": refined.get('refined_confidence', 0) / 100.0,
                "should_override": refined.get('should_override', False),
                "justification": refined.get('override_justification', '')
            }

        except Exception as e:
            logger.error(f"[parse_refinement] Failed to parse response: {str(e)}")
            return {"decision": None, "confidence": None, "should_override": False}

    def _extract_strengths(self, analysis: Dict[str, Any]) -> str:
        """Extract strengths from analysis."""
        positives = analysis.get('key_positives', [])
        if positives:
            return "\n".join([f"  - {p}" for p in positives])
        return "  None identified"

    def _extract_concerns(self, analysis: Dict[str, Any]) -> str:
        """Extract concerns from analysis."""
        risks = analysis.get('key_risks', [])
        if risks:
            return "\n".join([f"  - {r}" for r in risks])
        return "  None identified"

    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Return fallback analysis when LLM fails."""
        return {
            "analysis": {},
            "confidence": 0.0,
            "decision": "Review",
            "reasoning": "LLM analysis unavailable"
        }


def create_llm_reasoning_engine() -> LLMReasoningEngine:
    """Factory function to create LLM reasoning engine."""
    return LLMReasoningEngine()
