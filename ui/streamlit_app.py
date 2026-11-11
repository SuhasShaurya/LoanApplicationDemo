import streamlit as st
import httpx
import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 AI Loan Approval System")
st.markdown("Multi-Agent AI System for Automated Loan Application Analysis")

col1, col2 = st.columns([3, 1])
with col2:
    st.metric("Status", "🟢 Online")

tabs = st.tabs(["📋 Apply for Loan", "📊 View Applications", "📈 Dashboard", "📖 About"])

with tabs[0]:
    st.subheader("Loan Application Form")
    st.markdown("Enter applicant details below to submit a loan application")

    # Initialize session state for results
    if "application_result" not in st.session_state:
        st.session_state.application_result = None

    # Create form with user inputs
    with st.form("loan_application_form"):
        st.markdown("### Applicant Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            applicant_id = st.text_input(
                "Applicant ID",
                value="APP001",
                help="Unique identifier for the applicant"
            )
        with col2:
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=35,
                help="Age of the applicant"
            )
        with col3:
            income = st.number_input(
                "Annual Income ($)",
                min_value=10000,
                max_value=500000,
                value=75000,
                step=1000,
                help="Annual income in USD"
            )

        st.markdown("### Employment & Credit")

        col1, col2, col3 = st.columns(3)

        with col1:
            employment_type = st.selectbox(
                "Employment Type",
                ["Full-time", "Part-time", "Self-employed", "Contract", "Retired"],
                help="Type of employment"
            )
        with col2:
            credit_score = st.number_input(
                "Credit Score",
                min_value=300,
                max_value=850,
                value=750,
                help="Credit score (300-850)"
            )
        with col3:
            existing_liabilities = st.number_input(
                "Existing Liabilities ($)",
                min_value=0,
                max_value=500000,
                value=50000,
                step=1000,
                help="Total existing debts"
            )

        st.markdown("### Loan Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            loan_amount = st.number_input(
                "Loan Amount ($)",
                min_value=10000,
                max_value=1000000,
                value=250000,
                step=10000,
                help="Requested loan amount in USD"
            )
        with col2:
            loan_tenure_months = st.number_input(
                "Loan Tenure (Months)",
                min_value=12,
                max_value=360,
                value=240,
                step=12,
                help="Loan repayment period in months"
            )
        with col3:
            location = st.text_input(
                "Location",
                value="New York",
                help="Applicant's location/city"
            )

        # Submit button
        submitted = st.form_submit_button("Submit Application", use_container_width=True, type="primary")

    # Process form submission outside of form context
    if submitted:
        with st.spinner("🔄 Processing your loan application..."):
            try:
                # Prepare application data
                application_data = {
                    "applicant_id": applicant_id,
                    "age": int(age),
                    "income": float(income),
                    "employment_type": employment_type,
                    "credit_score": int(credit_score),
                    "loan_amount": float(loan_amount),
                    "loan_tenure_months": int(loan_tenure_months),
                    "existing_liabilities": float(existing_liabilities),
                    "location": location
                }

                # Send to API
                response = httpx.post(
                    f"http://{settings.API_HOST}:{settings.API_PORT}/apply-loan",
                    json=application_data,
                    timeout=30.0
                )

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.application_result = result

                    # MAIN DECISION DISPLAY - PROMINENT ON SCREEN
                    st.divider()

                    # Decision banner based on classification
                    decision_type = result.get("decision", result.get("classification", "Unknown"))

                    if decision_type == "Approve":
                        st.success("✅ LOAN APPLICATION APPROVED!", icon="✅")
                        decision_banner = """
                        ### 🟢 CONGRATULATIONS!
                        **Your loan application has been APPROVED!**

                        You are eligible for the requested loan amount.
                        Please proceed to complete the documentation.
                        """
                        banner_color = "#00FF00"
                    else:  # Reject
                        st.error("❌ LOAN APPLICATION REJECTED", icon="❌")
                        decision_banner = """
                        ### 🔴 APPLICATION REJECTED
                        **Unfortunately, your loan application has been REJECTED.**

                        Your financial profile does not meet our lending criteria at this time.
                        You may reapply after improving your financial situation.
                        """
                        banner_color = "#FF0000"

                    st.markdown(decision_banner)
                    st.divider()

                    # KEY METRICS DISPLAY
                    st.subheader("📊 Decision Metrics")

                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                    with metric_col1:
                        decision_emoji = {
                            "Approve": "✅",
                            "Reject": "❌",
                            "Review": "⏳"
                        }.get(decision_type, "❓")
                        st.metric("Decision Status", f"{decision_emoji} {decision_type}", delta=None)

                    with metric_col2:
                        risk_score = result.get("risk_score", 0)
                        risk_label = "Low ✓" if risk_score < 0.35 else "Moderate" if risk_score < 0.65 else "High"
                        st.metric("Risk Level", f"{risk_score:.2f}", delta=f"{risk_label}")

                    with metric_col3:
                        confidence = result.get("confidence", result.get("confidence_level", 0))
                        st.metric("Decision Confidence", f"{confidence:.0%}", delta=None)

                    with metric_col4:
                        case_id = result.get("case_id", "N/A")
                        st.metric("Case ID", case_id, delta=None)

                    st.divider()

                    # DECISION EXPLANATION
                    st.subheader("📋 Decision Summary")

                    explanation = result.get("explanation", "No explanation available")
                    st.info(f"**Decision Rationale:**\n\n{explanation}")

                    # KEY FACTORS
                    key_factors = result.get("key_decision_factors", [])
                    if key_factors:
                        st.subheader("🔍 Key Decision Factors")
                        for i, factor in enumerate(key_factors, 1):
                            st.write(f"{i}. {factor}")

                    st.divider()

                    # APPLICATION DETAILS
                    st.subheader("📝 Application Details")

                    detail_col1, detail_col2 = st.columns(2)

                    with detail_col1:
                        st.write("**Applicant Information**")
                        applicant_info = f"""
- **Applicant ID:** {result.get('applicant_id', 'N/A')}
- **Age:** {age} years
- **Location:** {location}
- **Employment:** {employment_type}
                        """
                        st.markdown(applicant_info)

                    with detail_col2:
                        st.write("**Application Information**")
                        app_info = f"""
- **Case ID:** {result.get('case_id', 'N/A')}
- **Application ID:** {result.get('application_id', 'N/A')}
- **Submission Time:** {result.get('timestamp', 'N/A')}
- **Status:** {decision_type}
                        """
                        st.markdown(app_info)

                    st.divider()

                    # FINANCIAL METRICS
                    st.subheader("💰 Financial Assessment")

                    fin_col1, fin_col2 = st.columns(2)

                    with fin_col1:
                        st.write("**Your Financial Profile**")
                        fin_profile = f"""
- **Annual Income:** ${income:,.0f}
- **Credit Score:** {credit_score}
- **Existing Liabilities:** ${existing_liabilities:,.0f}
- **Requested Loan:** ${loan_amount:,.0f}
- **Loan Tenure:** {loan_tenure_months} months
                        """
                        st.markdown(fin_profile)

                    with fin_col2:
                        st.write("**Risk Assessment**")
                        if "risk_analysis" in result:
                            risk_data = result.get("risk_analysis", {})
                            risk_assessment = f"""
- **DTI Ratio:** {risk_data.get('debt_to_income_ratio', 'N/A'):.2f}
- **Credit Risk Level:** {risk_data.get('credit_score_risk_level', 'N/A')}
- **Loan Amount Risk:** {risk_data.get('loan_amount_risk', 'N/A')}
- **Overall Financial Risk:** {risk_data.get('overall_financial_risk_score', 'N/A'):.2f}
                            """
                            st.markdown(risk_assessment)

                    st.divider()

                    # DETAILED ANALYSIS
                    st.subheader("🔬 Detailed Analysis")

                    with st.expander("📊 View Full Analysis Details"):
                        analysis_col1, analysis_col2 = st.columns(2)

                        with analysis_col1:
                            st.write("**Profile Analysis**")
                            profile = result.get("profile_analysis", {})
                            st.json(profile)

                        with analysis_col2:
                            st.write("**Risk Analysis**")
                            risk = result.get("risk_analysis", {})
                            st.json(risk)

                    st.divider()

                    # DOWNLOAD REPORT
                    st.subheader("📥 Download Report")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            label="📥 Download Decision Report (JSON)",
                            data=json.dumps(result, indent=2),
                            file_name=f"loan_decision_{result.get('case_id', 'unknown')}.json",
                            mime="application/json",
                            use_container_width=True
                        )

                    with col2:
                        # Generate text report
                        text_report = f"""
LOAN APPLICATION DECISION REPORT
Generated: {result.get('timestamp', 'N/A')}

DECISION: {decision_type}
Case ID: {result.get('case_id', 'N/A')}

APPLICANT INFORMATION:
- ID: {result.get('applicant_id', 'N/A')}
- Age: {age}
- Location: {location}
- Employment: {employment_type}

FINANCIAL INFORMATION:
- Annual Income: ${income:,.0f}
- Credit Score: {credit_score}
- Loan Amount: ${loan_amount:,.0f}
- Loan Tenure: {loan_tenure_months} months

DECISION METRICS:
- Risk Score: {result.get('risk_score', 'N/A'):.2f}
- Confidence: {confidence:.0%}

EXPLANATION:
{explanation}

KEY FACTORS:
{chr(10).join([f'- {factor}' for factor in key_factors])}
                        """
                        st.download_button(
                            label="📄 Download Decision Report (TXT)",
                            data=text_report,
                            file_name=f"loan_decision_{result.get('case_id', 'unknown')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                    st.divider()
                    st.success("✅ Your application has been processed successfully! Check the details above.")

                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")

            except httpx.ConnectError:
                st.error("❌ Cannot connect to API. Please ensure the FastAPI service is running on port 8000.")
                st.info("💡 To start the API, run: `python main.py`")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tabs[1]:
    st.subheader("📊 View Applications & Decisions")
    st.markdown("Review all submitted loan applications and their decisions")

    # Initialize session state for storing applications
    if "submitted_applications" not in st.session_state:
        st.session_state.submitted_applications = []

    # Add current result to history if available
    if st.session_state.application_result and st.session_state.application_result not in st.session_state.submitted_applications:
        st.session_state.submitted_applications.append(st.session_state.application_result)

    applications = st.session_state.submitted_applications

    if len(applications) == 0:
        st.info("📭 No applications submitted yet. Go to the 'Apply for Loan' tab to submit an application.")
    else:
        # Summary statistics
        st.markdown("### 📈 Application Summary")

        approved_count = sum(1 for app in applications if app.get("decision", app.get("classification")) == "Approve")
        rejected_count = sum(1 for app in applications if app.get("decision", app.get("classification")) == "Reject")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", len(applications))
        with col2:
            approval_rate = (approved_count / len(applications) * 100) if applications else 0
            st.metric("Approved ✅", f"{approved_count} ({approval_rate:.1f}%)")
        with col3:
            rejection_rate = (rejected_count / len(applications) * 100) if applications else 0
            st.metric("Rejected ❌", f"{rejected_count} ({rejection_rate:.1f}%)")

        st.divider()

        # Filter options
        st.markdown("### 🔍 Filter Applications")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            decision_filter = st.multiselect(
                "Filter by Decision",
                ["Approve", "Reject"],
                default=["Approve", "Reject"],
                key="decision_filter"
            )

        with filter_col2:
            search_term = st.text_input(
                "Search by Applicant ID or Case ID",
                placeholder="e.g., APP001 or CASE-001",
                key="search_term"
            )

        # Display search results prominently
        if search_term:
            st.divider()
            st.markdown("### 🔍 Search Results")

            matching_apps = [
                app for app in applications
                if search_term.lower() in (app.get("applicant_id", "").lower() + " " + app.get("case_id", "").lower())
            ]

            if matching_apps:
                for app in matching_apps:
                    decision = app.get("decision", app.get("classification", "Unknown"))
                    applicant_id = app.get("applicant_id", "Unknown")
                    case_id = app.get("case_id", "Unknown")
                    risk_score = app.get("risk_score", 0)
                    confidence = app.get("confidence", app.get("confidence_level", 0))

                    # Large status display - Only APPROVE or REJECT
                    if decision == "Approve":
                        st.success(f"✅ APPLICATION STATUS: APPROVED", icon="✅")
                        status_color = "green"
                        status_message = "APPROVED FOR LOAN DISBURSEMENT"
                    else:  # Reject
                        st.error(f"❌ APPLICATION STATUS: REJECTED", icon="❌")
                        status_color = "red"
                        status_message = "REJECTED - DOES NOT MEET LENDING CRITERIA"

                    # Main status info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Status", decision, delta=status_message)
                    with col2:
                        st.metric("Risk Score", f"{risk_score:.2f}", delta="High Risk" if risk_score > 0.6 else "Moderate" if risk_score > 0.35 else "Low Risk")
                    with col3:
                        st.metric("Confidence", f"{confidence:.0%}", delta="Very High" if confidence > 0.85 else "High")

                    st.divider()

                    # Detailed decision breakdown
                    st.markdown("### 📊 Decision Breakdown Based on Application Input")

                    breakdown_col1, breakdown_col2 = st.columns(2)

                    with breakdown_col1:
                        st.markdown("#### Input Information")
                        input_info = f"""
**Applicant Details:**
- ID: {app.get('applicant_id', 'N/A')}
- Age: {app.get('age', 'N/A')} years
- Location: {app.get('location', 'N/A')}

**Financial Information:**
- Annual Income: ${app.get('income', 0):,.0f}
- Credit Score: {app.get('credit_score', 'N/A')}
- Existing Liabilities: ${app.get('existing_liabilities', 0):,.0f}

**Employment:**
- Type: {app.get('employment_type', 'N/A')}

**Loan Request:**
- Loan Amount: ${app.get('loan_amount', 0):,.0f}
- Tenure: {app.get('loan_tenure_months', 'N/A')} months
                        """
                        st.write(input_info)

                    with breakdown_col2:
                        st.markdown("#### Decision Analysis")

                        if "profile_analysis" in app:
                            profile = app.get("profile_analysis", {})
                            analysis_info = f"""
**Income & Employment Assessment:**
- Income Stability Score: {profile.get('income_stability_score', 'N/A'):.2f}/1.0
- Employment Risk: {profile.get('employment_risk', 'N/A')}
- Profile Status: {'✅ Strong' if profile.get('income_stability_score', 0) > 0.75 else '⚠️ Moderate' if profile.get('income_stability_score', 0) > 0.5 else '❌ Weak'}
                            """
                            st.write(analysis_info)

                    st.divider()

                    # Risk analysis breakdown
                    st.markdown("### 💰 Risk Analysis (Why This Decision)")

                    if "risk_analysis" in app:
                        risk_data = app.get("risk_analysis", {})

                        risk_col1, risk_col2, risk_col3 = st.columns(3)

                        with risk_col1:
                            st.markdown("**Debt-to-Income (DTI)**")
                            dti = risk_data.get('debt_to_income_ratio', 0)
                            if dti < 0.30:
                                st.write(f"✅ {dti:.2f} - Healthy")
                            elif dti < 0.45:
                                st.write(f"⚠️ {dti:.2f} - Acceptable")
                            elif dti < 0.60:
                                st.write(f"⚠️ {dti:.2f} - High")
                            else:
                                st.write(f"❌ {dti:.2f} - Unaffordable")

                        with risk_col2:
                            st.markdown("**Credit Risk**")
                            credit_risk = risk_data.get('credit_score_risk_level', 'N/A')
                            credit_emoji = {
                                "Very Low": "✅",
                                "Low": "✅",
                                "Medium": "⚠️",
                                "High": "❌",
                                "Very High": "❌"
                            }.get(credit_risk, "❓")
                            st.write(f"{credit_emoji} {credit_risk}")

                        with risk_col3:
                            st.markdown("**Loan Amount Risk**")
                            loan_risk = risk_data.get('loan_amount_risk', 'N/A')
                            loan_emoji = {
                                "Low": "✅",
                                "Medium": "⚠️",
                                "High": "⚠️",
                                "Very High": "❌"
                            }.get(loan_risk, "❓")
                            st.write(f"{loan_emoji} {loan_risk}")

                    st.divider()

                    # Decision explanation
                    st.markdown("### 📋 Why This Decision Was Made")
                    explanation = app.get("explanation", "No detailed explanation available")
                    st.info(explanation)

                    # Key factors
                    st.markdown("### 🔑 Key Factors Affecting Decision")
                    key_factors = app.get("key_decision_factors", [])
                    if key_factors:
                        for i, factor in enumerate(key_factors, 1):
                            if "Strong" in factor or "Good" in factor or "Healthy" in factor or "Reasonable" in factor or "Stable" in factor:
                                st.write(f"✅ {i}. {factor}")
                            elif "Weak" in factor or "Poor" in factor or "High" in factor or "Unstable" in factor or "Excessive" in factor:
                                st.write(f"❌ {i}. {factor}")
                            else:
                                st.write(f"ℹ️ {i}. {factor}")

                    # Anomalies if any
                    if "risk_analysis" in app:
                        anomalies = app.get("risk_analysis", {}).get("anomalies_detected", [])
                        if anomalies:
                            st.markdown("### 🚩 Issues Detected")
                            for anomaly in anomalies:
                                st.write(f"⚠️ {anomaly}")

                    st.divider()

                    # Download option
                    st.markdown("### 📥 Download Application Report")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            label="📥 Download as JSON",
                            data=json.dumps(app, indent=2),
                            file_name=f"application_{case_id}_decision.json",
                            mime="application/json",
                            use_container_width=True
                        )

                    with col2:
                        summary_report = f"""
APPLICATION DECISION REPORT
═══════════════════════════════════════════════

STATUS: {decision.upper()}
Generated: {app.get('timestamp', 'N/A')}
Case ID: {case_id}

APPLICATION INFORMATION
───────────────────────────────────────────────
Applicant ID: {applicant_id}
Age: {app.get('age', 'N/A')}
Location: {app.get('location', 'N/A')}
Employment: {app.get('employment_type', 'N/A')}

FINANCIAL INFORMATION
───────────────────────────────────────────────
Annual Income: ${app.get('income', 0):,.0f}
Credit Score: {app.get('credit_score', 'N/A')}
Existing Liabilities: ${app.get('existing_liabilities', 0):,.0f}

LOAN REQUEST
───────────────────────────────────────────────
Loan Amount: ${app.get('loan_amount', 0):,.0f}
Tenure: {app.get('loan_tenure_months', 'N/A')} months

RISK METRICS
───────────────────────────────────────────────
Debt-to-Income Ratio: {app.get('risk_analysis', {}).get('debt_to_income_ratio', 'N/A'):.2f}
Credit Risk Level: {app.get('risk_analysis', {}).get('credit_score_risk_level', 'N/A')}
Loan Amount Risk: {app.get('risk_analysis', {}).get('loan_amount_risk', 'N/A')}
Overall Risk Score: {risk_score:.2f}
Decision Confidence: {confidence:.0%}

DECISION RATIONALE
───────────────────────────────────────────────
{explanation}

KEY FACTORS
───────────────────────────────────────────────
{chr(10).join([f'{i}. {factor}' for i, factor in enumerate(key_factors, 1)])}

DECISION OUTCOME
───────────────────────────────────────────────
Status: {status_message}
Confidence: {confidence:.0%}
Risk Level: {'High' if risk_score > 0.6 else 'Moderate' if risk_score > 0.35 else 'Low'}
                        """
                        st.download_button(
                            label="📄 Download as TXT",
                            data=summary_report,
                            file_name=f"application_{case_id}_decision.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                    st.divider()

            else:
                st.warning(f"❌ No applications found matching: '{search_term}'")
                st.info("Try searching with different ID or check the application list below")

        st.divider()

        # Filter applications
        filtered_applications = [
            app for app in applications
            if (app.get("decision", app.get("classification")) in decision_filter or
                app.get("classification") in decision_filter)
            and (not search_term or search_term.lower() in
                 (app.get("applicant_id", "").lower() + " " + app.get("case_id", "").lower()))
        ]

        if len(filtered_applications) == 0:
            st.warning("❌ No applications match your filter criteria.")
        else:
            st.markdown(f"### 📋 Displaying {len(filtered_applications)} Application(s)")

            # Display each application in an expandable container
            for idx, app in enumerate(filtered_applications, 1):
                decision = app.get("decision", app.get("classification", "Unknown"))
                applicant_id = app.get("applicant_id", "Unknown")
                case_id = app.get("case_id", "Unknown")
                risk_score = app.get("risk_score", 0)
                confidence = app.get("confidence", app.get("confidence_level", 0))

                # Color code based on decision
                decision_emoji = {
                    "Approve": "✅",
                    "Reject": "❌"
                }.get(decision, "❓")

                # Create expander header
                header_text = f"{decision_emoji} {decision.upper()} | Applicant: {applicant_id} | Case: {case_id}"

                with st.expander(header_text, expanded=False):
                    # Decision outcome display
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Decision", f"{decision_emoji} {decision}")
                    with col2:
                        st.metric("Risk Score", f"{risk_score:.2f}")
                    with col3:
                        st.metric("Confidence", f"{confidence:.0%}")

                    st.divider()

                    # Application details
                    detail_tab1, detail_tab2, detail_tab3, detail_tab4 = st.tabs(
                        ["📝 Decision", "💰 Financial", "📊 Details", "📥 Report"]
                    )

                    with detail_tab1:
                        st.markdown("### Decision Outcome")

                        # Decision banner
                        if decision == "Approve":
                            st.success(f"✅ Application APPROVED")
                            st.write(app.get("explanation", "No explanation available"))
                        elif decision == "Reject":
                            st.error(f"❌ Application REJECTED")
                            st.write(app.get("explanation", "No explanation available"))
                        else:
                            st.warning(f"⚠️ Application Requires REVIEW")
                            st.write(app.get("explanation", "No explanation available"))

                        st.markdown("### Key Decision Factors")
                        key_factors = app.get("key_decision_factors", [])
                        if key_factors:
                            for i, factor in enumerate(key_factors, 1):
                                st.write(f"{i}. {factor}")
                        else:
                            st.write("No specific factors documented")

                    with detail_tab2:
                        st.markdown("### Financial Assessment")

                        if "risk_analysis" in app:
                            risk_data = app.get("risk_analysis", {})

                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Risk Metrics**")
                                st.write(f"• DTI Ratio: {risk_data.get('debt_to_income_ratio', 'N/A'):.2f}" if isinstance(risk_data.get('debt_to_income_ratio'), (int, float)) else f"• DTI Ratio: {risk_data.get('debt_to_income_ratio', 'N/A')}")
                                st.write(f"• Credit Risk: {risk_data.get('credit_score_risk_level', 'N/A')}")
                                st.write(f"• Loan Risk: {risk_data.get('loan_amount_risk', 'N/A')}")
                                st.write(f"• Overall Risk: {risk_data.get('overall_financial_risk_score', 'N/A'):.2f}" if isinstance(risk_data.get('overall_financial_risk_score'), (int, float)) else f"• Overall Risk: {risk_data.get('overall_financial_risk_score', 'N/A')}")

                            with col2:
                                st.write("**Anomalies Detected**")
                                anomalies = risk_data.get("anomalies_detected", [])
                                if anomalies:
                                    for anomaly in anomalies:
                                        st.write(f"🚩 {anomaly}")
                                else:
                                    st.write("✓ No anomalies detected")

                    with detail_tab3:
                        st.markdown("### Application Details")

                        if "profile_analysis" in app:
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("**Applicant Profile**")
                                profile = app.get("profile_analysis", {})
                                st.write(f"• ID: {profile.get('applicant_id', 'N/A')}")
                                st.write(f"• Age: {profile.get('age', 'N/A')}")
                                st.write(f"• Income: ${profile.get('annual_income', 0):,.0f}" if isinstance(profile.get('annual_income'), (int, float)) else f"• Income: {profile.get('annual_income', 'N/A')}")
                                st.write(f"• Employment: {profile.get('employment_type', 'N/A')}")
                                st.write(f"• Income Stability: {profile.get('income_stability_score', 'N/A'):.2f}" if isinstance(profile.get('income_stability_score'), (int, float)) else f"• Income Stability: {profile.get('income_stability_score', 'N/A')}")
                                st.write(f"• Employment Risk: {profile.get('employment_risk', 'N/A')}")

                            with col2:
                                st.write("**Loan Details**")
                                loan_data = {
                                    "Loan Amount": app.get("loan_amount"),
                                    "Loan Tenure": app.get("loan_tenure_months"),
                                    "Existing Liabilities": app.get("existing_liabilities"),
                                    "Location": app.get("location"),
                                    "Case ID": app.get("case_id"),
                                    "Timestamp": app.get("timestamp")
                                }
                                for key, value in loan_data.items():
                                    if key in ["Loan Amount", "Existing Liabilities"]:
                                        st.write(f"• {key}: ${value:,.0f}" if isinstance(value, (int, float)) else f"• {key}: {value}")
                                    elif key == "Loan Tenure":
                                        st.write(f"• {key}: {value} months")
                                    else:
                                        st.write(f"• {key}: {value}")

                    with detail_tab4:
                        st.markdown("### Download Application Report")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.download_button(
                                label="📥 Download as JSON",
                                data=json.dumps(app, indent=2),
                                file_name=f"application_{case_id}.json",
                                mime="application/json",
                                use_container_width=True
                            )

                        with col2:
                            # Generate summary report
                            summary_report = f"""
APPLICATION SUMMARY REPORT
Generated: {app.get('timestamp', 'N/A')}

DECISION OUTCOME
───────────────────────────────────────
Decision: {decision}
Case ID: {case_id}
Applicant ID: {applicant_id}
Risk Score: {risk_score:.2f}
Confidence: {confidence:.0%}

APPLICANT INFORMATION
───────────────────────────────────────
Age: {app.get('age', 'N/A')}
Location: {app.get('location', 'N/A')}
Employment: {app.get('employment_type', 'N/A')}
Annual Income: ${app.get('income', 0):,.0f}

LOAN DETAILS
───────────────────────────────────────
Loan Amount: ${app.get('loan_amount', 0):,.0f}
Loan Tenure: {app.get('loan_tenure_months', 'N/A')} months
Existing Liabilities: ${app.get('existing_liabilities', 0):,.0f}
Credit Score: {app.get('credit_score', 'N/A')}

DECISION EXPLANATION
───────────────────────────────────────
{app.get('explanation', 'No explanation available')}

KEY FACTORS
───────────────────────────────────────
{chr(10).join([f'{i}. {factor}' for i, factor in enumerate(app.get('key_decision_factors', []), 1)])}

FINANCIAL METRICS
───────────────────────────────────────
Risk Analysis:
{json.dumps(app.get('risk_analysis', {}), indent=2)}

Profile Analysis:
{json.dumps(app.get('profile_analysis', {}), indent=2)}
                            """
                            st.download_button(
                                label="📄 Download as TXT",
                                data=summary_report,
                                file_name=f"application_{case_id}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )

                st.divider()

with tabs[2]:
    st.subheader("📈 System Dashboard")

    st.markdown("### System Performance & Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Agents", 4)
    with col2:
        st.metric("MCP Servers", 4)
    with col3:
        st.metric("Decision Types", 3)

    st.divider()

    st.subheader("System Components")
    st.markdown("""
    **Architecture Layers:**
    - 🎨 Presentation Layer: Streamlit UI
    - 🔌 Microservice Layer: FastAPI REST API
    - 🔄 Orchestration Layer: Loan Processing Engine
    - 🧠 Agent Layer: 4 Domain-Specific Agents
    - 📡 Communication Layer: MCP Servers

    **4 Independent Agents:**
    1. **Applicant Profile Agent** - Analyzes demographics & income stability
    2. **Financial Risk Agent** - Evaluates financial metrics & risk
    3. **Loan Decision Agent** - Synthesizes analysis & makes decision
    4. **Compliance Agent** - Logs decisions & executes actions

    **Decision Outcomes:**
    - ✅ **APPROVE** - Loan approved for disbursement
    - ❌ **REJECT** - Loan rejected due to risk factors
    - 🔍 **REVIEW** - Requires manual review by underwriter
    """)

    st.divider()
    st.subheader("Input Parameters")
    st.markdown("""
    The system analyzes the following applicant information:

    | Parameter | Range | Unit |
    |-----------|-------|------|
    | Age | 18-100 | years |
    | Annual Income | $10K-$500K | USD |
    | Credit Score | 300-850 | score |
    | Loan Amount | $10K-$1M | USD |
    | Loan Tenure | 12-360 | months |
    | Existing Liabilities | $0-$500K | USD |
    | Employment Type | Full-time, Part-time, Self-employed, Contract, Retired | - |
    | Location | Any city/region | text |
    """)

with tabs[3]:
    st.subheader("📖 About this System")

    st.markdown("""
### Multi-Agent Agentic AI Loan Approval System

This system demonstrates a distributed microservices-based Agentic AI architecture for automating loan application analysis.

#### Architecture Layers

1. **Presentation Layer**: Streamlit chatbot UI
2. **Microservice Layer**: FastAPI REST endpoints
3. **Orchestration Layer**: LangGraph-based orchestration engine
4. **Agent Layer**: 4 domain-specific agents
5. **Communication Layer**: MCP servers

#### Key Agents

- **Applicant Profile Agent**: Evaluates applicant demographics and income stability
- **Financial Risk Agent**: Analyzes financial metrics and risk indicators
- **Loan Decision Agent**: Synthesizes analysis into approval/rejection decision
- **Compliance & Action Agent**: Executes actions and sends notifications

#### Decision Outputs

- **Approve**: Loan is approved for fund disbursement
- **Reject**: Loan is rejected due to risk factors
- **Review**: Application requires manual review by underwriter

#### Technology Stack

- Frontend: Streamlit
- Backend: FastAPI
- Orchestration: LangGraph, LangChain
- MCP Framework: FastMCP
- LLM: Anthropic Claude Sonnet 4.6
    """)

st.divider()
st.caption("Loan Approval System v1.0 | Powered by Anthropic Claude")
