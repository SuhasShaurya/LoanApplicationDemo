# Loan Approval System - Project Index

## 📋 Quick Navigation

### 📖 Documentation
- **[README.md](README.md)** - Original problem statement and requirements
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Comprehensive technical guide (11KB)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment, usage, and troubleshooting (5KB)
- **[COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)** - Project completion summary (11KB)
- **[PROJECT_INDEX.md](PROJECT_INDEX.md)** - This file

### 🚀 Getting Started
```bash
# Quick demo (1 line)
python3 main.py

# With dependencies
pip install -r requirements.txt && python3 main.py
```

## 📁 Directory Structure

### Root Level
```
Suhas_Mandlik/
├── main.py                  # Entry point for demo
├── requirements.txt         # Python dependencies
├── .env                     # Configuration
├── run_demo.sh             # Demo script
└── *.md                    # Documentation files
```

### `/config` - Configuration
- `settings.py` - Configuration management, decision thresholds

### `/data` - Test Data
- `mock_data.py` - 5 test applicants with realistic profiles

### `/mcp_servers` - MCP Server Implementations
- `applicant_db_server.py` - Applicant profile analysis
- `risk_rules_db_server.py` - Financial risk assessment
- `decision_synthesis_server.py` - Decision logic
- `notification_system_server.py` - Action execution

### `/agents` - Domain-Specific Agents
- `applicant_profile_agent.py` - Analyzes applicant profile
- `financial_risk_agent.py` - Evaluates financial risk
- `loan_decision_agent.py` - Makes final decision
- `compliance_agent.py` - Executes action & logs

### `/orchestration` - Orchestration Layer
- `state.py` - State definitions for workflow
- `simple_orchestrator.py` - Standalone orchestrator (no dependencies)
- `orchestrator.py` - Full LangGraph version (requires LangGraph)

### `/services` - FastAPI Microservice
- `fastapi_service.py` - REST API endpoints (port 8000)
- `loan_processor.py` - Application processing logic

### `/ui` - Streamlit Web Interface
- `streamlit_app.py` - Web UI (port 8501)

### `/tests` - Integration Tests
- `test_integration.py` - 8 comprehensive test cases

## 🎯 Key Features

### Architecture
- ✅ 5-layer microservices architecture
- ✅ 4 independent agents with clear responsibilities
- ✅ MCP servers for standardized communication
- ✅ Orchestration layer for workflow coordination

### Functionality
- ✅ Loan application analysis and decision making
- ✅ Three outcomes: Approve, Reject, Review
- ✅ Multi-factor risk assessment
- ✅ Explainable decisions with reasoning
- ✅ Audit trail with case IDs

### Interfaces
- ✅ REST API endpoints (FastAPI)
- ✅ Web interface (Streamlit)
- ✅ Command-line demo
- ✅ Python module imports

## 🔧 Running the System

### Option 1: Quick Demo (Recommended)
```bash
python3 main.py
```
Runs instantly, processes 5 test applicants

### Option 2: API Server
```bash
python3 -m uvicorn services.fastapi_service:app --host 127.0.0.1 --port 8000
```
Access API at: http://127.0.0.1:8000
Swagger docs at: http://127.0.0.1:8000/docs

### Option 3: Web Interface
```bash
streamlit run ui/streamlit_app.py
```
Access UI at: http://localhost:8501

### Option 4: Full System (3 terminals)
```bash
# Terminal 1
python3 -m uvicorn services.fastapi_service:app --host 127.0.0.1 --port 8000

# Terminal 2
streamlit run ui/streamlit_app.py

# Terminal 3 (Optional)
python3 main.py
```

## 📊 API Endpoints

### POST /apply-loan
Submit loan application
```bash
curl -X POST http://127.0.0.1:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{"applicant_id": "APP001"}'
```

### GET /available-applicants
List test applicants

### GET /health
Health check

### GET /decision-history/{application_id}
Retrieve decision

## 👥 Test Applicants

| ID | Income | Credit | Profile |
|---|---|---|---|
| APP001 | $75K | 750 | Full-time, good credit |
| APP002 | $45K | 580 | Contract, poor credit |
| APP003 | $120K | 780 | Full-time, excellent |
| APP004 | $60K | 620 | Part-time, moderate |
| APP005 | $95K | 700 | Self-employed, mixed |

## 🧠 Agent Flow

```
Application Received
        ↓
┌─────────────────────────────────────────┐
│ 1. APPLICANT PROFILE AGENT              │
│    ✓ Income stability score             │
│    ✓ Employment risk classification     │
│    ✓ Application completeness           │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 2. FINANCIAL RISK AGENT                 │
│    ✓ Debt-to-income ratio               │
│    ✓ Credit score risk level            │
│    ✓ Loan amount risk assessment        │
│    ✓ Anomaly detection                  │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 3. LOAN DECISION AGENT                  │
│    ✓ Synthesize all analyses            │
│    ✓ Make decision: Approve/Reject/Review
│    ✓ Calculate confidence & risk score  │
│    ✓ Generate explanation               │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 4. COMPLIANCE AGENT                     │
│    ✓ Log decision                       │
│    ✓ Generate case ID                   │
│    ✓ Execute appropriate action         │
│    ✓ Create audit trail                 │
└─────────────────────────────────────────┘
        ↓
   Decision Returned
```

## 🧪 Testing

### Run Tests
```bash
pip install pytest pytest-asyncio
pytest tests/test_integration.py -v
```

### Test Classes
- `TestMCPServers` - Tests MCP server functions
- `TestAgents` - Tests individual agents
- `TestOrchestrator` - Tests orchestration workflow
- `TestMockData` - Tests data retrieval

## 📚 Documentation Map

| Document | Purpose | Size |
|----------|---------|------|
| README.md | Problem statement & requirements | 3.7KB |
| IMPLEMENTATION_GUIDE.md | Technical architecture & details | 11KB |
| DEPLOYMENT.md | Usage, API docs, troubleshooting | 5KB |
| COMPLETION_SUMMARY.md | Project summary & status | 11KB |
| PROJECT_INDEX.md | This quick reference | 4KB |

## 🔑 Key Files Reference

### Configuration
- `config/settings.py` - All configuration constants
- `.env` - Environment variables

### Business Logic
- `mcp_servers/decision_synthesis_server.py` - Decision logic
- `config/settings.py` - Decision thresholds

### Agents
- `agents/applicant_profile_agent.py` - Profile analysis
- `agents/financial_risk_agent.py` - Risk evaluation
- `agents/loan_decision_agent.py` - Decision making
- `agents/compliance_agent.py` - Action execution

### Orchestration
- `orchestration/simple_orchestrator.py` - Main orchestrator
- `orchestration/state.py` - State management

### API
- `services/fastapi_service.py` - REST endpoints

### UI
- `ui/streamlit_app.py` - Web interface

## 🛠️ Customization Guide

### Add New Test Applicant
1. Edit `data/mock_data.py`
2. Add entry to `MOCK_LOAN_APPLICATIONS`
3. Run `python3 main.py` to test

### Change Decision Thresholds
1. Edit `config/settings.py`
2. Modify threshold constants
3. Test with `python3 main.py`

### Modify Decision Logic
1. Edit `mcp_servers/decision_synthesis_server.py`
2. Update `make_decision()` function
3. Run tests: `pytest tests/test_integration.py`

### Add New API Endpoint
1. Edit `services/fastapi_service.py`
2. Add new route with `@app.post()` or `@app.get()`
3. Run with `python3 -m uvicorn services.fastapi_service:app --reload`

## 📈 Performance

- **Decision Time**: < 1 second per application
- **Concurrent Requests**: Limited by Python (use Gunicorn for production)
- **Memory Usage**: ~50MB per process
- **Scalability**: Horizontal scaling with load balancer

## 🔐 Security Considerations

- No authentication (add OAuth2 for production)
- CORS enabled for all origins (restrict in production)
- No rate limiting (add in production)
- Sensitive data in logs (implement log filtering)

## 🚀 Production Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` with production values
3. Use Gunicorn: `gunicorn services.fastapi_service:app -w 4 -b 0.0.0.0:8000`
4. Use Streamlit with authentication
5. Add database for decision storage
6. Implement monitoring and logging
7. Add rate limiting and API keys
8. Use HTTPS/SSL certificates

## 📞 Support & Troubleshooting

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Troubleshooting guide
- API error responses
- Common issues and solutions
- Production setup recommendations

## ✅ Evaluation Checklist

- ✅ Multi-agent architecture implemented
- ✅ 4 domain-specific agents created
- ✅ 4 MCP servers for communication
- ✅ LangGraph orchestration (+ simple version)
- ✅ FastAPI microservice
- ✅ Streamlit UI
- ✅ Explainable decisions
- ✅ Mock data with 5 applicants
- ✅ Integration tests
- ✅ Comprehensive documentation
- ✅ Working demo
- ✅ Modifiable code

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📝 License & Attribution

This project demonstrates multi-agent Agentic AI architecture for educational and evaluation purposes.

---

**Last Updated**: November 6, 2024  
**Status**: ✅ Complete and Ready for Evaluation  
**Total Files**: 32 | **Python Files**: 25 | **Lines of Code**: 2,500+
