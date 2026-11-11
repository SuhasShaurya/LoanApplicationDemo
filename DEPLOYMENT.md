# Deployment and Usage Guide

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure Environment**:
Edit `.env` file with your settings:
```env
ANTHROPIC_API_KEY=your_key_here  # Optional, for LLM integration
API_HOST=127.0.0.1
API_PORT=8000
STREAMLIT_PORT=8501
```

## Usage Scenarios

### Scenario 1: Quick Demo
Perfect for testing the system quickly:
```bash
python3 main.py
```
**Output**: Processes 5 test applicants and shows decisions

### Scenario 2: API Integration
For integrating with other systems:
```bash
python3 -m uvicorn services.fastapi_service:app --host 0.0.0.0 --port 8000
```
Then make POST requests to `/apply-loan` endpoint

### Scenario 3: Interactive UI
For end-user interface:
```bash
streamlit run ui/streamlit_app.py
```
Access at `http://localhost:8501`

### Scenario 4: Full System
All components running:
```bash
# Terminal 1
python3 -m uvicorn services.fastapi_service:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2
streamlit run ui/streamlit_app.py

# Terminal 3 (optional)
python3 main.py
```

## API Documentation

### Endpoint: POST /apply-loan

**Request**:
```bash
curl -X POST http://127.0.0.1:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{"applicant_id": "APP001"}'
```

**Response** (200 OK):
```json
{
  "application_id": "F31774A5",
  "applicant_id": "APP001",
  "decision": "Review",
  "risk_score": 0.60,
  "confidence": 0.70,
  "explanation": "Application requires manual review due to mixed signals...",
  "case_id": "A6DC9A0D",
  "timestamp": "2024-11-06T12:34:56.789012",
  "profile_analysis": {
    "income_stability_score": 1.00,
    "employment_risk": "Low",
    "annual_income": 75000.0
  },
  "risk_analysis": {
    "debt_to_income_ratio": 0.83,
    "credit_score_risk_level": "Very Low",
    "loan_amount_risk": "Medium"
  }
}
```

### Endpoint: GET /available-applicants

```bash
curl http://127.0.0.1:8000/available-applicants
```

**Response**:
```json
{
  "applicants": [
    {
      "applicant_id": "APP001",
      "name": "Applicant APP001",
      "income": 75000,
      "credit_score": 750
    },
    ...
  ]
}
```

### Endpoint: GET /health

```bash
curl http://127.0.0.1:8000/health
```

## Testing the Workflow

### Test Case 1: Good Credit (Likely Approve)
```bash
curl -X POST http://127.0.0.1:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{"applicant_id": "APP001"}'
```

### Test Case 2: Poor Credit (Likely Reject)
```bash
curl -X POST http://127.0.0.1:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{"applicant_id": "APP002"}'
```

### Test Case 3: Mixed Profile (Likely Review)
```bash
curl -X POST http://127.0.0.1:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{"applicant_id": "APP005"}'
```

## Monitoring and Debugging

### Check API Health
```bash
curl http://127.0.0.1:8000/health
```

### View API Documentation
Visit `http://127.0.0.1:8000/docs` (Swagger UI)

### Debug Mode
Enable detailed logging:
```bash
LOG_LEVEL=DEBUG python3 main.py
```

## Performance Metrics

- Average processing time: < 1 second
- Agents invoked: 4 in sequence
- Decision accuracy: Deterministic based on rules
- Scalability: Linear with request volume

## Customization

### Adding New Applicant
Edit `data/mock_data.py`:
```python
{
    "applicant_id": "APP006",
    "age": 35,
    "income": 80000.0,
    "employment_type": "Full-time",
    "credit_score": 700,
    "loan_amount": 300000.0,
    "loan_tenure_months": 240,
    "existing_liabilities": 50000.0,
    "location": "Austin",
}
```

### Adjusting Decision Thresholds
Edit `config/settings.py`:
```python
MIN_INCOME_STABILITY_SCORE = 0.5
MAX_DEBT_TO_INCOME_RATIO = 0.5
MIN_CREDIT_SCORE = 600
MIN_CONFIDENCE_THRESHOLD = 0.6
```

### Modifying Decision Logic
Edit `mcp_servers/decision_synthesis_server.py` function `make_decision()`

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### API Connection Error from UI
Ensure FastAPI server is running on port 8000

## Production Deployment

For production use:

1. **Use environment variables** instead of .env file
2. **Enable CORS** appropriately in `fastapi_service.py`
3. **Add authentication** to API endpoints
4. **Use process manager** (gunicorn, systemd)
5. **Enable logging** to file/cloud service
6. **Add rate limiting** and throttling
7. **Use load balancer** for multiple instances
8. **Implement database** for decision storage
9. **Add monitoring** and alerting

## Support

For issues or questions:
1. Check the IMPLEMENTATION_GUIDE.md
2. Review test cases in tests/test_integration.py
3. Check API documentation at /docs endpoint
4. Examine logs for error messages
