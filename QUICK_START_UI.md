# Quick Start - See Decision on Screen

## 🚀 Get the System Running in 3 Steps

### Step 1: Verify the System Works

```bash
cd /home/ubuntu/Desktop/Suhas_Mandlik
python3 test_loan_decision.py
```

Expected output:
```
TEST SUMMARY: 7 passed, 0 failed
```

✅ If all tests pass, continue to Step 2

---

### Step 2: Start the FastAPI Backend

**In Terminal #1:**

```bash
cd /home/ubuntu/Desktop/Suhas_Mandlik
python3 main.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ Leave this running and open a new terminal

---

### Step 3: Start the Streamlit Frontend

**In Terminal #2:**

```bash
cd /home/ubuntu/Desktop/Suhas_Mandlik
streamlit run ui/streamlit_app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

✅ Your browser should automatically open, or visit: **http://localhost:8501**

---

## 📱 Using the UI to See Decisions

### Step 1: Open the Application Tab

Click the **"📋 Apply for Loan"** tab (should be already open)

### Step 2: Fill in the Application Form

**Example 1: Strong Applicant (Will be APPROVED)**

```
Applicant ID: APP001
Age: 35
Annual Income ($): 85000
Employment Type: Full-time
Credit Score: 760
Loan Amount ($): 200000
Loan Tenure (Months): 360
Existing Liabilities ($): 2500
Location: California
```

### Step 3: Click "Submit Application"

Click the blue **"Submit Application"** button

### Step 4: See the Decision!

You'll immediately see:

```
✅ LOAN APPLICATION APPROVED!

🟢 CONGRATULATIONS!
Your loan application has been APPROVED!

📊 Decision Metrics

Decision Status: ✅ Approve     Risk Level: 0.15 (Low ✓)
Decision Confidence: 88%        Case ID: CASE-XXXXX

📋 Decision Summary

Loan APPROVED - Applicant demonstrates strong financial capacity...

🔍 Key Decision Factors
1. Strong income stability
2. Stable employment
3. Healthy debt-to-income ratio
4. Good credit profile
5. Reasonable loan amount

[Scroll down for more details...]
```

---

## 📊 Try Different Scenarios

### Scenario 2: Weak Applicant (Will be REJECTED)

```
Applicant ID: APP002
Age: 28
Annual Income ($): 35000
Employment Type: Self-employed
Credit Score: 550
Loan Amount ($): 280000
Loan Tenure (Months): 240
Existing Liabilities ($): 6000
Location: Texas
```

**Result:** ❌ **REJECTED** with high risk

### Scenario 3: Mixed Signals (Will be REVIEW)

```
Applicant ID: APP003
Age: 32
Annual Income ($): 55000
Employment Type: Part-time
Credit Score: 680
Loan Amount ($): 150000
Loan Tenure (Months): 300
Existing Liabilities ($): 3500
Location: New York
```

**Result:** ⚠️ **REQUIRES REVIEW**

---

## 🎯 What You'll See on Screen

Once you submit an application, the screen displays (from top to bottom):

### 1. Decision Banner (Prominent)
```
✅ LOAN APPLICATION APPROVED!
or
❌ LOAN APPLICATION REJECTED
or
⚠️ APPLICATION REQUIRES REVIEW
```

### 2. Key Metrics (4 Cards)
```
Decision Status     Risk Level      Confidence      Case ID
✅ Approve         0.15 (Low ✓)     88%             CASE-001
```

### 3. Decision Summary
Explanation of why the decision was made

### 4. Key Decision Factors
List of factors that influenced the decision

### 5. Application Details
All information you submitted

### 6. Financial Assessment
Your financial profile and risk metrics

### 7. Detailed Analysis (Expandable)
Technical JSON data

### 8. Download Buttons
```
📥 Download Decision Report (JSON)
📄 Download Decision Report (TXT)
```

---

## 🔄 Full Workflow Example

### Input Screen (Step 1)
```
┌─────────────────────────────────────┐
│ 📋 Apply for Loan Tab Active        │
│                                     │
│ Applicant ID:     [APP001]          │
│ Age:              [35]              │
│ Annual Income:    [85000]           │
│ Employment Type:  [Full-time]       │
│ Credit Score:     [760]             │
│ Loan Amount:      [200000]          │
│ Loan Tenure:      [360]             │
│ Existing Liabil:  [2500]            │
│ Location:         [California]      │
│                                     │
│ [Submit Application] ← Click Here   │
└─────────────────────────────────────┘
```

### Processing (Step 2)
```
🔄 Processing your loan application...
```

### Decision Display (Step 3)
```
✅ LOAN APPLICATION APPROVED!

🟢 CONGRATULATIONS!

📊 Decision Metrics
├─ Decision: ✅ Approve
├─ Risk: 0.15 (Low)
├─ Confidence: 88%
└─ Case ID: CASE-XXXXX

📋 Decision Summary
"Loan APPROVED - Strong financial profile..."

🔍 Key Factors
1. Strong income stability
2. Stable employment
3. Healthy DTI ratio
4. Good credit profile
5. Reasonable loan amount

💰 Financial Assessment
├─ Income: $85,000
├─ Credit: 760
├─ DTI: 0.11
└─ Risk: 0.15

📥 Download Reports
├─ [Download JSON]
└─ [Download TXT]
```

---

## ✅ Success Indicators

**✅ System is working if:**

- [ ] Tests pass: `python3 test_loan_decision.py` → 7/7 passing
- [ ] API starts: `python3 main.py` → "Uvicorn running on http://127.0.0.1:8000"
- [ ] UI loads: `streamlit run ui/streamlit_app.py` → Opens at localhost:8501
- [ ] Form displays: See application form on the screen
- [ ] Decision shows: After clicking "Submit", see decision banner

---

## 🛠️ Troubleshooting

### Q: Tests don't pass
```bash
python3 test_loan_decision.py
```
A: Check Python version (need 3.7+) and dependencies

### Q: API won't start
```bash
python3 main.py
```
A: Check if port 8000 is already in use:
```bash
lsof -i :8000  # See what's using port 8000
kill -9 <PID>   # Kill the process
```

### Q: UI won't load
```bash
streamlit run ui/streamlit_app.py
```
A: Check if port 8501 is free or install streamlit:
```bash
pip install streamlit
```

### Q: "Cannot connect to API" error
A: Make sure both terminals are running:
- Terminal 1: `python3 main.py` (backend)
- Terminal 2: `streamlit run ui/streamlit_app.py` (frontend)

### Q: Decision doesn't display
A: Check browser console for errors (F12) and ensure API is responding

---

## 📋 Terminal Setup

For easy management, use multiple terminal tabs:

**Tab 1: Backend API**
```bash
cd /home/ubuntu/Desktop/Suhas_Mandlik
python3 main.py
```
(Keep running)

**Tab 2: Frontend UI**
```bash
cd /home/ubuntu/Desktop/Suhas_Mandlik
streamlit run ui/streamlit_app.py
```
(Keep running)

**Tab 3: Testing/Development**
```bash
cd /home/ubuntu/Desktop/Suhas_Mandlik
# Run tests, check logs, etc.
python3 test_loan_decision.py
```

---

## 🎓 Test All Decision Types

After starting the UI, try these to see all decision types:

### Test 1: APPROVAL ✅
```
Input: 35yo, $85k, Full-time, Credit 760
Click: Submit Application
Result: ✅ APPROVED screen shows
```

### Test 2: REJECTION ❌
```
Input: 28yo, $35k, Self-employed, Credit 550
Click: Submit Application
Result: ❌ REJECTED screen shows
```

### Test 3: REVIEW ⚠️
```
Input: 32yo, $55k, Part-time, Credit 680
Click: Submit Application
Result: ⚠️ REVIEW screen shows
```

---

## 📊 Dashboard Tab

Click the **"📊 Dashboard"** tab to see system information:

- System components overview
- 4 Independent agents
- Decision types explanation
- Input parameters reference

---

## 📖 About Tab

Click the **"📖 About"** tab to learn:

- System architecture
- Agent descriptions
- Decision outputs
- Technology stack

---

## 🎯 Next Steps

1. ✅ Run tests: `python3 test_loan_decision.py`
2. ✅ Start backend: `python3 main.py` (Terminal 1)
3. ✅ Start frontend: `streamlit run ui/streamlit_app.py` (Terminal 2)
4. ✅ Open browser: **http://localhost:8501**
5. ✅ Fill form and submit to see decision!

---

## 📸 Expected Screenshots

### When UI Loads
```
🏦 AI Loan Approval System
Multi-Agent AI System for Automated Loan Application Analysis

[Status: 🟢 Online]

📋 Apply for Loan | 📊 Dashboard | 📖 About
```

### After Submission
```
✅ LOAN APPLICATION APPROVED!

🟢 CONGRATULATIONS!
Your loan application has been APPROVED!

📊 Decision Metrics
Decision: ✅ Approve | Risk: 0.15 | Confidence: 88% | Case ID: XXXXX

📋 Decision Summary
[Explanation text...]

🔍 Key Decision Factors
1. Strong income stability
2. Stable employment
...
```

---

## 💡 Pro Tips

1. **Batch Testing:** Try multiple applicants in sequence
2. **Download Reports:** Download each decision for comparison
3. **Check Different Ages:** See how age affects decisions
4. **Vary Credit Scores:** Test boundary conditions (600, 650, 700, 750)
5. **Try Edge Cases:** Extreme DTI, very young, very old applicants

---

## ✅ Checklist

Before starting, ensure:

- [ ] Python 3.7+ installed
- [ ] In correct directory: `/home/ubuntu/Desktop/Suhas_Mandlik`
- [ ] Tests pass: `python3 test_loan_decision.py`
- [ ] Ports 8000 & 8501 are free
- [ ] Two terminal windows open
- [ ] Dependencies installed (streamlit, fastapi, etc.)

---

## 🚀 Ready?

```bash
# Step 1: Verify
python3 test_loan_decision.py

# Step 2: Start API (Terminal 1)
python3 main.py

# Step 3: Start UI (Terminal 2)
streamlit run ui/streamlit_app.py

# Step 4: Open Browser
# http://localhost:8501

# Step 5: See Decision on Screen! 🎉
```

**Enjoy the Loan Decision System!** 🎉
