# Loan Decision System - Quick Reference

## Decision Matrix at a Glance

### APPROVE ✅ (Score < 0.35)
```
✓ Credit Score: 700+
✓ DTI Ratio: < 0.35
✓ Income Stability: > 0.75
✓ Employment: Full-time
✓ Age: 21-75
✓ Anomalies: 0-1 minor
```
**Confidence:** 0.85-0.95  |  **Risk:** 0.10-0.20

---

### REVIEW ⚠️ (Score 0.35-0.55)
```
? Credit Score: 650-700 (Medium)
? DTI Ratio: 0.35-0.60 (Moderate)
? Income Stability: 0.40-0.75 (Moderate)
? Employment: Part-time/Mixed
? Anomalies: 1-2 detected
```
**Confidence:** 0.60-0.75  |  **Risk:** 0.40-0.60

---

### REJECT ❌ (Score > 0.55)
```
✗ Credit Score: < 600 (Very High Risk)
✗ DTI Ratio: > 0.60 (Unaffordable)
✗ Income Stability: < 0.40 (Very Low)
✗ Financial Risk: > 0.70
✗ Anomalies: > 3 critical
```
**Confidence:** 0.80-0.95  |  **Risk:** 0.70-0.95

---

## Key Scoring Formulas

### Overall Composite Score
```
Score = (Credit 0.35) + (Income -0.25) + (DTI 0.25) 
      + (Employment 0.10) + (Loan 0.05)
```

### Debt-to-Income Ratio
```
DTI = (Monthly Loan Payment + Monthly Liabilities) / Monthly Income

Good:   < 0.30
OK:     0.30-0.45
High:   0.45-0.60
Bad:    > 0.60
```

### Income Stability Score
| Employment | Base | Bonus@35+ | Total |
|---|---|---|---|
| Full-time | 0.90 | +0.10 | 1.0 |
| Retired | 0.70 | — | 0.7 |
| Part-time | 0.60 | — | 0.6 |
| Self-emp | 0.50 | — | 0.5 |
| Contract | 0.40 | — | 0.4 |

---

## Anomaly Flags

| Flag | Severity | Threshold |
|------|----------|-----------|
| Low Credit | 🔴 Critical | < 600 |
| High DTI | 🔴 Critical | > 0.50 |
| Young Age | 🟡 Medium | < 21 |
| Old Age | 🟡 Medium | > 75 |
| Unstable Job | 🟡 Medium | Self-emp/Contract |
| Very High LTI | 🔴 Critical | > 4.0 |
| Incomplete App | 🟡 Medium | Missing fields |

---

## Credit Score Risk Map

| Score | Risk | Value |
|---|---|---|
| 750+ | Very Low | 0.10 |
| 700-749 | Low | 0.25 |
| 650-699 | Medium | 0.50 |
| 600-649 | High | 0.75 |
| < 600 | Very High | 0.95 |

---

## Loan-to-Income Risk Map

| Ratio | Risk | Value |
|---|---|---|
| ≤ 2.0 | Low | 0.20 |
| 2.1-3.0 | Medium | 0.50 |
| 3.1-4.0 | High | 0.75 |
| > 4.0 | Very High | 0.95 |

---

## Decision Tree Logic

```
START: New Application
  │
  ├─→ Credit Score < 600?
  │   └─→ YES: REJECT ❌ (Risk 0.95, Conf 0.92)
  │
  ├─→ DTI > 0.60?
  │   └─→ YES: REJECT ❌ (Risk 0.80, Conf 0.88)
  │
  ├─→ Financial Risk > 0.70?
  │   └─→ YES: REJECT ❌ (Risk 0.85, Conf 0.90)
  │
  ├─→ Composite Score > 0.55?
  │   └─→ YES: REJECT ❌ (Risk 0.78, Conf 0.85)
  │
  ├─→ Composite Score < 0.35?
  │   └─→ YES: APPROVE ✅ (Risk 0.15, Conf 0.88)
  │
  └─→ REVIEW ⚠️ (Risk 0.45, Conf 0.70)
```

---

## Input Validation Rules

```python
Required Fields:
  ✓ applicant_id: Non-empty string
  ✓ age: 21-75 integer
  ✓ income: > 0 float
  ✓ employment_type: Valid type
  ✓ credit_score: 300-850 integer
  ✓ loan_amount: > 0 float
  ✓ loan_tenure_months: > 0 integer
  ✓ existing_liabilities: ≥ 0 float
  ✓ location: Non-empty string
```

---

## Agent Communication Flow

```
1. UI collects applicant data
2. FastAPI validates input
3. Applicant Profile Agent analyzes:
   - Income stability
   - Employment risk
4. Financial Risk Agent calculates:
   - DTI ratio
   - Credit risk
   - Anomalies
5. Decision Synthesis Agent:
   - Weights all factors
   - Applies thresholds
   - Generates decision
6. Notification System:
   - Sends notification
   - Logs decision
7. UI displays result
```

---

## Output JSON Structure

```json
{
  "applicant_id": "string",
  "classification": "Approve|Reject|Review",
  "risk_score": 0.0-1.0,
  "confidence_level": 0.0-1.0,
  "key_decision_factors": ["string"],
  "explanation": "string",
  "decision_reasoning": {
    "primary_factors": ["string"],
    "approval_criteria": {
      "meets_minimum_income_stability": boolean,
      "acceptable_dti_ratio": boolean,
      "credit_score_acceptable": boolean,
      "employment_stable": boolean,
      "acceptable_financial_risk": boolean
    },
    "decision_basis": "string"
  }
}
```

---

## Thresholds at a Glance

| Metric | Poor | Acceptable | Good | Excellent |
|--------|------|-----------|------|-----------|
| **Credit** | <600 | 600-699 | 700-749 | 750+ |
| **DTI** | >0.60 | 0.45-0.60 | 0.30-0.45 | <0.30 |
| **Income Stability** | <0.40 | 0.40-0.60 | 0.60-0.85 | >0.85 |
| **LTI** | >4.0 | 3.0-4.0 | 2.0-3.0 | <2.0 |

---

## Test Commands

```bash
# Run all tests
python test_loan_decision.py

# Run specific test
python -c "from test_loan_decision import test_approval_case; test_approval_case()"

# View sample outputs
cat LOAN_DECISION_GUIDE.md | grep -A 20 "Scenario"
```

---

## Common Scenarios & Outcomes

### Scenario 1: Young Professional ✅
- Age: 28, Income: $70k, Full-time
- Credit: 710, DTI: 0.30, Loan: $150k
- **Result: APPROVE** (Score 0.32, Conf 0.88)

### Scenario 2: High Debt ❌
- Age: 35, Income: $50k, Full-time
- Credit: 680, DTI: 0.65, Loan: $200k
- **Result: REJECT** (Score 0.62, Conf 0.85)

### Scenario 3: Mixed Signals ⚠️
- Age: 32, Income: $60k, Part-time
- Credit: 680, DTI: 0.45, Loan: $150k
- **Result: REVIEW** (Score 0.48, Conf 0.68)

### Scenario 4: Senior Professional ✅
- Age: 52, Income: $120k, Full-time
- Credit: 780, DTI: 0.25, Loan: $250k
- **Result: APPROVE** (Score 0.25, Conf 0.92)

### Scenario 5: Bad Credit ❌
- Age: 45, Income: $55k, Full-time
- Credit: 550, DTI: 0.35, Loan: $120k
- **Result: REJECT** (Score 0.58, Conf 0.88)

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Always APPROVE | Scoring broken | Check weights sum to 1.0 |
| Always REJECT | Thresholds wrong | Verify score ranges |
| Missing factors | Incomplete data | Validate input fields |
| Wrong decision | Logic error | Review decision tree |
| High variance | Weighting off | Recalibrate weights |

---

## Files Reference

| File | Purpose |
|------|---------|
| `applicant_db_server.py` | Profile analysis |
| `risk_rules_db_server.py` | Risk metrics |
| `decision_synthesis_server.py` | Decision logic |
| `loan_decision_agent.py` | Agent orchestration |
| `test_loan_decision.py` | Test suite |
| `LOAN_DECISION_GUIDE.md` | Detailed guide |
| `IMPLEMENTATION_SUMMARY.md` | Full architecture |

---

**Quick Start:** `python test_loan_decision.py`  
**Full Docs:** See `LOAN_DECISION_GUIDE.md`  
**Architecture:** See `IMPLEMENTATION_SUMMARY.md`
