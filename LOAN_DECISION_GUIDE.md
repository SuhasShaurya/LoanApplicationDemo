# Loan Decision Implementation Guide

## Overview
This guide explains how the loan approval system makes decisions (Approve/Reject/Review) based on applicant information.

## Decision Flow

```
Applicant Data
    ↓
┌─────────────────────────────────────┐
│ 1. Profile Analysis Agent            │
│    - Income Stability Score          │
│    - Employment Risk Classification  │
│    - Application Completeness Check  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. Financial Risk Analysis Agent     │
│    - Debt-to-Income Ratio            │
│    - Credit Score Risk Level         │
│    - Loan Amount Risk                │
│    - Anomaly Detection               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Decision Synthesis Engine         │
│    - Weighted Scoring System         │
│    - Decision Thresholds             │
│    - Confidence Calculation          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ FINAL DECISION                       │
│ - Approve                            │
│ - Reject                             │
│ - Review (Manual)                    │
└─────────────────────────────────────┘
```

## Input Parameters Required

### Applicant Profile
```python
{
    "applicant_id": "APP001",
    "age": 35,
    "income": 60000,                    # Annual income in USD
    "employment_type": "Full-time",     # Full-time, Part-time, Self-employed, Contract, Retired
    "credit_score": 720,                # Credit score (300-850)
    "loan_amount": 150000,              # Requested loan amount
    "loan_tenure_months": 360,          # Loan tenure in months
    "existing_liabilities": 5000,       # Monthly existing debt obligations
    "location": "California"            # State/Province
}
```

## Decision Criteria

### 1. APPROVAL CRITERIA ✅
A loan is **APPROVED** when:
- **Credit Risk**: Low or Very Low (Credit Score ≥ 700)
- **Income Stability**: Strong (Score ≥ 0.75)
- **Debt-to-Income Ratio**: Healthy (< 0.35)
- **Employment Risk**: Low
- **Overall Financial Risk Score**: < 0.35
- **No Critical Anomalies**: Max 1 minor anomaly

**Confidence Level**: 0.85-0.95
**Risk Score**: 0.10-0.20

### 2. REJECTION CRITERIA ❌
A loan is **REJECTED** when:
- **Credit Risk**: Very High or High (Credit Score < 600)
- **Overall Financial Risk Score**: > 0.70
- **Debt-to-Income Ratio**: Critical (> 0.60)
- **Income Stability**: Very Low (Score < 0.40)
- **Multiple Critical Anomalies**: > 3 significant issues detected

**Confidence Level**: 0.80-0.95
**Risk Score**: 0.70-0.95

### 3. MANUAL REVIEW REQUIRED ⚠️
A loan **REQUIRES REVIEW** when:
- Mixed financial signals detected
- Credit Risk: Medium (Score 650-700)
- Debt-to-Income Ratio: Moderate (0.35-0.60)
- Income Stability: Moderate (0.40-0.75)
- Employment Risk: Medium
- 1-2 Detected Anomalies
- Financial Risk Score: 0.35-0.70

**Confidence Level**: 0.60-0.75
**Risk Score**: 0.40-0.60

## Decision Logic - Weighted Scoring

The system uses a **weighted composite score** (0-1 scale):

```
Overall Score = 
  (Credit Risk Score × 0.35) +           # Most important: credit history
  (1 - Income Stability × 0.25) +        # Important: income reliability
  (DTI Score × 0.25) +                   # Important: debt capacity
  (Employment Risk Score × 0.10) +       # Moderate: employment stability
  (Loan Risk Score × 0.05)               # Minor: loan amount appropriateness
```

**Decision Thresholds**:
- **Score < 0.35** → **APPROVE** (High Confidence)
- **Score 0.35-0.55** → **REVIEW** (Manual Review)
- **Score > 0.55** → **REJECT** (High Confidence)

## Risk Assessment Breakdown

### Credit Score Classification
| Score Range | Risk Level | Score Value |
|------------|-----------|------------|
| 750+ | Very Low | 0.10 |
| 700-749 | Low | 0.25 |
| 650-699 | Medium | 0.50 |
| 600-649 | High | 0.75 |
| < 600 | Very High | 0.95 |

### Income Stability Classification
| Employment Type | Stability Score |
|-----------------|-----------------|
| Full-time | 0.90 (+0.10 bonus if age ≥ 35) |
| Retired | 0.70 |
| Part-time | 0.60 |
| Self-employed | 0.50 |
| Contract | 0.40 |

### Employment Risk Classification
| Type | Risk |
|------|------|
| Full-time | Low |
| Retired | Medium |
| Part-time | Medium |
| Self-employed | High |
| Contract | High |

### Loan-to-Income Ratio Risk
| Ratio | Risk Level |
|-------|-----------|
| ≤ 2.0 | Low |
| 2.1-3.0 | Medium |
| 3.1-4.0 | High |
| > 4.0 | Very High |

## Anomaly Detection

The system flags the following as anomalies:
1. **High DTI** (> 0.5) - Cannot afford monthly payments
2. **Low Credit Score** (< 600) - Bad credit history
3. **Age Below 21** - Legal/experience concerns
4. **Age Above 75** - Repayment risk (retirement)
5. **Unstable Employment** - Self-employed, Contract, Part-time
6. **Very High Loan Amount** - Loan-to-income > 4.0
7. **Incomplete Application** - Missing required fields

## Output Decision Response

```python
{
    "applicant_id": "APP001",
    "classification": "Approve",                    # Approve | Reject | Review
    "risk_score": 0.18,                            # 0.0-1.0 (higher = more risky)
    "confidence_level": 0.88,                      # 0.0-1.0 (decision confidence)
    "key_decision_factors": [
        "Strong income stability",
        "Stable employment",
        "Healthy debt-to-income ratio",
        "Good credit profile"
    ],
    "explanation": "Loan APPROVED - Applicant demonstrates strong financial capacity...",
    "decision_reasoning": {
        "primary_factors": [...],
        "approval_criteria": {
            "meets_minimum_income_stability": true,
            "acceptable_dti_ratio": true,
            "credit_score_acceptable": true,
            "employment_stable": true,
            "acceptable_financial_risk": true
        },
        "decision_basis": "Based on weighted analysis..."
    }
}
```

## Example Scenarios

### Scenario 1: APPROVAL ✅
```python
applicant = {
    "applicant_id": "APP001",
    "age": 35,
    "income": 80000,
    "employment_type": "Full-time",
    "credit_score": 750,
    "loan_amount": 200000,
    "loan_tenure_months": 360,
    "existing_liabilities": 2000,
    "location": "New York"
}
```
**Result**: APPROVE
- Income Stability: 1.0 (Full-time + age 35)
- DTI: 0.27 (Good)
- Credit Risk: Very Low (750+)
- Employment Risk: Low
- **Overall Score**: 0.28 → **APPROVE**

### Scenario 2: REJECTION ❌
```python
applicant = {
    "applicant_id": "APP002",
    "age": 65,
    "income": 30000,
    "employment_type": "Self-employed",
    "credit_score": 580,
    "loan_amount": 300000,
    "loan_tenure_months": 180,
    "existing_liabilities": 8000,
    "location": "Texas"
}
```
**Result**: REJECT
- Income Stability: 0.5 (Self-employed)
- DTI: 0.77 (Very High)
- Credit Risk: Very High (580)
- Loan-to-Income: 10.0 (Very High)
- **Overall Score**: 0.68 → **REJECT**
- **Anomalies**: 3 detected (age, low credit, high DTI, unstable employment)

### Scenario 3: REVIEW ⚠️
```python
applicant = {
    "applicant_id": "APP003",
    "age": 28,
    "income": 50000,
    "employment_type": "Contract",
    "credit_score": 680,
    "loan_amount": 150000,
    "loan_tenure_months": 300,
    "existing_liabilities": 3000,
    "location": "California"
}
```
**Result**: REVIEW
- Income Stability: 0.4 (Contract)
- DTI: 0.42 (Moderate)
- Credit Risk: Medium (680)
- Employment Risk: High (Contract)
- **Overall Score**: 0.47 → **REVIEW**
- **Reason**: Mixed signals - needs manual assessment

## System Output Fields

| Field | Type | Description |
|-------|------|-------------|
| applicant_id | string | Unique applicant identifier |
| classification | string | Final decision: Approve/Reject/Review |
| risk_score | float | 0.0-1.0 where 1.0 is highest risk |
| confidence_level | float | 0.0-1.0 confidence in the decision |
| key_decision_factors | list | Top factors influencing decision |
| explanation | string | Human-readable decision summary |
| decision_reasoning | dict | Detailed reasoning with criteria checks |

## Integration Points

### Agent Layer
- **Applicant Profile Agent**: Calculates income stability & employment risk
- **Financial Risk Agent**: Calculates DTI, credit risk, and anomalies
- **Decision Synthesis Agent**: Makes final Approve/Reject/Review decision
- **Compliance Agent**: Handles notifications and case tracking

### API Integration
All components work through MCP servers:
- `applicant_db_server.py` - Profile analysis
- `risk_rules_db_server.py` - Risk metrics
- `decision_synthesis_server.py` - Decision logic
- `notification_system_server.py` - Notifications

## Key Thresholds

| Metric | Poor | Acceptable | Good | Excellent |
|--------|------|-----------|------|-----------|
| Credit Score | <600 | 600-699 | 700-749 | 750+ |
| DTI Ratio | >0.60 | 0.45-0.60 | 0.30-0.45 | <0.30 |
| Income Stability | <0.40 | 0.40-0.60 | 0.60-0.85 | >0.85 |
| Loan-to-Income | >4.0 | 3.0-4.0 | 2.0-3.0 | <2.0 |

## Compliance & Regulations

The system ensures:
- ✅ Fair lending practices (no discrimination based on protected attributes)
- ✅ Explainable AI (clear reasoning for every decision)
- ✅ Audit trail (full decision history with timestamps)
- ✅ Consistent criteria application across all applicants
- ✅ Appeal process support (detailed decision factors for review)

---
*Last Updated: 2024*
*Version: 1.0*
