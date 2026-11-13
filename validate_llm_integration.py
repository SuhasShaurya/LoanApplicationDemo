#!/usr/bin/env python3
"""Validate LLM integration and workflow structure."""
import sys
import json

try:
    print("[✓] Testing imports...")
    from orchestration.langgraph_orchestrator import EnhancedLoanOrchestrator, create_enhanced_orchestrator
    print("[✓] EnhancedLoanOrchestrator imported successfully")

    from orchestration.llm_reasoning import LLMReasoningEngine, create_llm_reasoning_engine
    print("[✓] LLMReasoningEngine imported successfully")

    from orchestration.state import LoanApplicationState
    print("[✓] LoanApplicationState imported successfully")

    print("\n[✓] Testing orchestrator creation...")
    orchestrator = create_enhanced_orchestrator()
    print("[✓] Orchestrator created successfully")

    print("\n[✓] Checking workflow structure...")
    graph = orchestrator.get_workflow_graph()
    print(f"[✓] Workflow has {len(graph['nodes'])} nodes:")
    for i, node in enumerate(graph['nodes'], 1):
        print(f"    {i}. {node}")

    print(f"\n[✓] Workflow has {len(graph['edges'])} edges")

    print("\n[✓] Validating new LLM nodes...")
    assert 'llm_analysis' in graph['nodes'], "llm_analysis node not found"
    assert 'refinement_decision' in graph['nodes'], "refinement_decision node not found"
    print("[✓] Both LLM nodes present in workflow")

    print("\n[✓] Checking state fields...")
    state = LoanApplicationState(
        application_id="TEST-001",
        applicant_id="APPL-001",
        applicant_data={}
    )
    state_dict = state.to_dict()
    required_fields = [
        'llm_analysis',
        'llm_analysis_enabled',
        'refined_decision',
        'llm_decision_refined',
        'requires_manual_review'
    ]
    for field in required_fields:
        assert field in state_dict, f"Missing field: {field}"
        print(f"    ✓ {field}")

    print("\n[✓] All validation checks passed!")
    print("\n" + "="*60)
    print("LLM INTEGRATION VALIDATION COMPLETE")
    print("="*60)
    print("\nWorkflow Structure:")
    print(json.dumps({
        'nodes': graph['nodes'],
        'node_count': len(graph['nodes']),
        'edge_count': len(graph['edges']),
        'llm_enabled': True
    }, indent=2))

except Exception as e:
    print(f"[✗] Validation failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
