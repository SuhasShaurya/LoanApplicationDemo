"""Main entry point for the Loan Approval System."""
import asyncio
from data.mock_data import MOCK_LOAN_APPLICATIONS
from orchestration.simple_orchestrator import create_simple_orchestrator

async def main():
    """Run the loan approval system with sample data."""
    print("=" * 60)
    print("Loan Approval System - Multi-Agent Demo")
    print("=" * 60)

    orchestrator = create_simple_orchestrator()

    for idx, applicant_data in enumerate(MOCK_LOAN_APPLICATIONS, 1):
        print(f"\n[{idx}] Processing Application for {applicant_data['applicant_id']}")
        print("-" * 60)

        try:
            result = await orchestrator.process_loan_application(applicant_data)

            print(f"Application ID: {result['application_id']}")
            print(f"Applicant ID: {result['applicant_id']}")
            print(f"Decision: {result['decision']}")
            print(f"Risk Score: {result['risk_score']:.2f}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Case ID: {result['case_id']}")
            print(f"Explanation: {result['explanation']}")

            if result['profile_analysis']:
                print(f"\nProfile Analysis:")
                print(f"  - Income Stability: {result['profile_analysis'].get('income_stability_score', 'N/A'):.2f}")
                print(f"  - Employment Risk: {result['profile_analysis'].get('employment_risk', 'N/A')}")

            if result['risk_analysis']:
                print(f"\nRisk Analysis:")
                print(f"  - DTI Ratio: {result['risk_analysis'].get('debt_to_income_ratio', 'N/A'):.2f}")
                print(f"  - Credit Risk: {result['risk_analysis'].get('credit_score_risk_level', 'N/A')}")

        except Exception as e:
            print(f"Error processing application: {str(e)}")

    print("\n" + "=" * 60)
    print("Demo Completed")
    print("=" * 60)
    print("\nTo start the API server, run: python -m uvicorn services.fastapi_service:app --host 127.0.0.1 --port 8000")
    print("To start the Streamlit UI, run: streamlit run ui/streamlit_app.py")

if __name__ == "__main__":
    asyncio.run(main())
