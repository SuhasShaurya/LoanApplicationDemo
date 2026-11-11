#!/bin/bash

echo "================================"
echo "Loan Approval System - Demo"
echo "================================"
echo ""

cd "$(dirname "$0")"

echo "[1/3] Running core demonstration..."
python main.py

echo ""
echo "[2/3] To start the FastAPI server:"
echo "  python -m uvicorn services.fastapi_service:app --host 127.0.0.1 --port 8000 --reload"
echo ""
echo "[3/3] To start the Streamlit UI (in another terminal):"
echo "  streamlit run ui/streamlit_app.py"
echo ""
echo "Or run all components in parallel:"
echo "  1. Terminal 1: python -m uvicorn services.fastapi_service:app --host 127.0.0.1 --port 8000 --reload"
echo "  2. Terminal 2: streamlit run ui/streamlit_app.py"
echo "  3. Terminal 3: python main.py"
