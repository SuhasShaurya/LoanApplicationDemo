"""Workflow visualization and tracing utilities for LangGraph orchestrator with LLM observability."""
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from orchestration.state import LoanApplicationState


class LLMObservabilityCollector:
    """Collect and analyze LLM-specific metrics and events."""

    def __init__(self):
        """Initialize observability collector."""
        self.events: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {
            "total_llm_calls": 0,
            "total_tokens_used": 0,
            "total_cost": 0.0,
            "llm_latency_total": 0.0,
            "refinements_triggered": 0,
            "decisions_overridden": 0,
            "errors_caught": 0,
        }
        self.start_time = time.time()

    def record_llm_call(self, event: Dict[str, Any]):
        """Record an LLM API call event.

        Args:
            event: Event dictionary with 'type', 'timestamp', 'method', 'tokens', 'cost', 'latency'
        """
        self.events.append(event)
        self.metrics["total_llm_calls"] += 1
        self.metrics["total_tokens_used"] += event.get("tokens", 0)
        self.metrics["total_cost"] += event.get("cost", 0.0)
        self.metrics["llm_latency_total"] += event.get("latency", 0.0)

    def record_refinement(self, event: Dict[str, Any]):
        """Record a borderline case refinement event.

        Args:
            event: Refinement event with 'initial_confidence', 'refined_confidence', 'override'
        """
        self.events.append(event)
        self.metrics["refinements_triggered"] += 1
        if event.get("should_override"):
            self.metrics["decisions_overridden"] += 1

    def record_error(self, event: Dict[str, Any]):
        """Record an LLM error event.

        Args:
            event: Error event with 'error_type', 'error_message'
        """
        self.events.append(event)
        self.metrics["errors_caught"] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get observability summary.

        Returns:
            Summary dictionary with metrics and analysis
        """
        elapsed_time = time.time() - self.start_time
        avg_latency = (self.metrics["llm_latency_total"] / self.metrics["total_llm_calls"]
                      if self.metrics["total_llm_calls"] > 0 else 0)

        return {
            "timestamp": datetime.now().isoformat(),
            "elapsed_time": elapsed_time,
            "metrics": self.metrics,
            "averages": {
                "avg_latency_per_call": avg_latency,
                "avg_tokens_per_call": (self.metrics["total_tokens_used"] / self.metrics["total_llm_calls"]
                                       if self.metrics["total_llm_calls"] > 0 else 0),
                "refinement_rate": (self.metrics["refinements_triggered"] / self.metrics["total_llm_calls"]
                                   if self.metrics["total_llm_calls"] > 0 else 0),
                "override_rate": (self.metrics["decisions_overridden"] / self.metrics["refinements_triggered"]
                                 if self.metrics["refinements_triggered"] > 0 else 0),
            },
            "event_count": len(self.events)
        }


class WorkflowVisualizer:
    """Utilities for visualizing and tracing workflow execution."""

    @staticmethod
    def export_to_mermaid(graph_structure: Dict[str, Any]) -> str:
        """Export workflow graph as Mermaid diagram including LLM nodes.

        Args:
            graph_structure: Graph structure from orchestrator.get_workflow_graph()

        Returns:
            Mermaid diagram string
        """
        mermaid = "graph TD\n"

        # Add nodes with LLM-specific styling
        node_labels = {
            "applicant_profile": "📋 Profile Analysis",
            "financial_risk": "💰 Financial Risk",
            "loan_decision": "✓ Loan Decision",
            "llm_analysis": "🧠 LLM Analysis",
            "refinement_decision": "🔄 Refinement",
            "route_decision": "🛣️ Route Decision",
            "compliance_action": "✅ Compliance",
            "manual_review": "👤 Manual Review",
            "error_handler": "⚠️ Error Handler",
            "finalize": "📤 Finalize",
            "END": "🏁 End"
        }

        # Add nodes with styling
        llm_nodes = {"llm_analysis", "refinement_decision"}
        for node in graph_structure.get("nodes", []):
            label = node_labels.get(node, node)
            if node in llm_nodes:
                mermaid += f"    {node}[\"{label}\"]:::llm_node\n"
            else:
                mermaid += f"    {node}[\"{label}\"]\n"

        mermaid += "\n"

        # Add edges
        for src, dst in graph_structure.get("edges", []):
            mermaid += f"    {src} --> {dst}\n"

        # Add styling
        mermaid += "\n    classDef llm_node fill:#e1f5ff,stroke:#01579b,stroke-width:3px,color:#000\n"

        return mermaid

    @staticmethod
    def export_to_svg(graph_structure: Dict[str, Any]) -> str:
        """Export workflow graph as SVG (requires graphviz).

        Note: This is a placeholder. Full SVG export would require
        graphviz library. Use Mermaid diagram for now.
        """
        return "SVG export requires graphviz library. Use Mermaid for now."

    @staticmethod
    def format_execution_trace(
        execution_trace: List[Dict[str, Any]],
        application_id: str
    ) -> str:
        """Format execution trace as human-readable report.

        Args:
            execution_trace: Execution trace from orchestrator
            application_id: Application ID for reference

        Returns:
            Formatted trace report
        """
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                    EXECUTION TRACE REPORT                      ║
║ Application ID: {application_id:<48}║
║ Generated: {datetime.now().isoformat():<51}║
╚════════════════════════════════════════════════════════════════╝

Execution Timeline:
─────────────────────────────────────────────────────────────────
"""
        for i, entry in enumerate(execution_trace, 1):
            timestamp = entry.get("timestamp", "unknown")
            node = entry.get("node", "unknown")
            status = entry.get("status", "unknown")
            attempt = entry.get("attempt", 1)

            status_icon = "✓" if status == "success" else "✗"
            attempt_info = f" (attempt {attempt})" if attempt > 1 else ""

            report += f"{i:2}. [{timestamp}] {status_icon} {node:<25} {status}{attempt_info}\n"

        report += "─────────────────────────────────────────────────────────────────\n"
        return report

    @staticmethod
    def export_execution_trace(
        execution_trace: List[Dict[str, Any]],
        filename: str = None
    ) -> str:
        """Export execution trace to JSON file.

        Args:
            execution_trace: Execution trace from orchestrator
            filename: Output filename (default: trace_<timestamp>.json)

        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trace_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(execution_trace, f, indent=2)

        return filename

    @staticmethod
    def get_statistics(execution_trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics from execution trace.

        Args:
            execution_trace: Execution trace from orchestrator

        Returns:
            Statistics dictionary
        """
        if not execution_trace:
            return {
                "total_nodes_executed": 0,
                "successful_nodes": 0,
                "failed_nodes": 0,
                "total_attempts": 0,
                "max_retries": 0
            }

        node_stats = {}
        total_attempts = 0
        successful = 0
        failed = 0
        max_retries = 0

        for entry in execution_trace:
            node = entry.get("node", "unknown")
            status = entry.get("status", "unknown")
            attempt = entry.get("attempt", 1)

            if node not in node_stats:
                node_stats[node] = {"success": 0, "failed": 0, "attempts": 0}

            total_attempts += 1
            if status == "success":
                successful += 1
                node_stats[node]["success"] += 1
            else:
                failed += 1
                node_stats[node]["failed"] += 1

            node_stats[node]["attempts"] = attempt
            max_retries = max(max_retries, attempt - 1)

        return {
            "total_nodes_executed": len(node_stats),
            "successful_nodes": successful,
            "failed_nodes": failed,
            "total_attempts": total_attempts,
            "max_retries": max_retries,
            "average_attempts": total_attempts / len(node_stats) if node_stats else 0,
            "node_details": node_stats
        }

    @staticmethod
    def print_workflow_structure(graph_structure: Dict[str, Any]):
        """Print workflow structure in human-readable format.

        Args:
            graph_structure: Graph structure from orchestrator
        """
        print("\n" + "="*70)
        print("WORKFLOW STRUCTURE")
        print("="*70)

        print("\nNodes:")
        print("-" * 70)
        for i, node in enumerate(graph_structure.get("nodes", []), 1):
            print(f"  {i}. {node}")

        print("\nEdges (Flow):")
        print("-" * 70)
        edges = graph_structure.get("edges", [])
        for src, dst in edges:
            print(f"  {src} → {dst}")

        print("\n" + "="*70 + "\n")

    @staticmethod
    def print_execution_trace(
        execution_trace: List[Dict[str, Any]],
        application_id: str = "N/A"
    ):
        """Print execution trace in human-readable format.

        Args:
            execution_trace: Execution trace from orchestrator
            application_id: Application ID for reference
        """
        print("\n" + "="*70)
        print(f"EXECUTION TRACE - Application: {application_id}")
        print("="*70)

        for i, entry in enumerate(execution_trace, 1):
            timestamp = entry.get("timestamp", "unknown")
            node = entry.get("node", "unknown")
            status = entry.get("status", "unknown")
            attempt = entry.get("attempt", 1)

            status_icon = "✓" if status == "success" else "✗"
            attempt_info = f" [attempt {attempt}]" if attempt > 1 else ""

            print(f"  {i:2}. {status_icon} {node:<25} {status:<10} {timestamp}{attempt_info}")

        # Print statistics
        stats = WorkflowVisualizer.get_statistics(execution_trace)
        print("\n" + "-"*70)
        print("STATISTICS:")
        print("-"*70)
        print(f"  Total nodes executed: {stats['total_nodes_executed']}")
        print(f"  Successful: {stats['successful_nodes']}")
        print(f"  Failed: {stats['failed_nodes']}")
        print(f"  Total attempts: {stats['total_attempts']}")
        print(f"  Max retries: {stats['max_retries']}")
        print(f"  Average attempts per node: {stats['average_attempts']:.2f}")
        print("\n" + "="*70 + "\n")


class LLMDecisionAnalyzer:
    """Analyze and explain LLM-powered decisions with reasoning transparency."""

    @staticmethod
    def analyze_llm_reasoning(llm_analysis: Dict[str, Any]) -> str:
        """Analyze and format LLM chain-of-thought reasoning.

        Args:
            llm_analysis: LLM analysis dictionary from state

        Returns:
            Formatted reasoning analysis
        """
        analysis = "\n╔════════════════════════════════════════════════════════════════╗"
        analysis += "\n║              LLM CHAIN-OF-THOUGHT ANALYSIS                    ║"
        analysis += "\n╚════════════════════════════════════════════════════════════════╝\n"

        if not llm_analysis:
            return analysis + "No LLM analysis available.\n"

        # Decision and confidence
        analysis += f"\n🧠 LLM Decision: {llm_analysis.get('decision', 'N/A')}"
        analysis += f"\n   Confidence: {llm_analysis.get('confidence', 0):.1%}\n"

        # Chain-of-thought steps
        steps = llm_analysis.get('reasoning_steps', [])
        if steps:
            analysis += "\n📋 Reasoning Steps (6-Step Framework):\n"
            analysis += "─" * 66 + "\n"
            for i, step in enumerate(steps, 1):
                analysis += f"  Step {i}: {step}\n"

        # Decision factors
        factors = llm_analysis.get('factors', {})
        if factors:
            analysis += "\n─" * 66 + "\n"
            positive = factors.get('positive', [])
            concerns = factors.get('concerns', [])

            if positive:
                analysis += "\n✅ Positive Factors:\n"
                for factor in positive:
                    analysis += f"   • {factor}\n"

            if concerns:
                analysis += "\n⚠️ Concerns:\n"
                for factor in concerns:
                    analysis += f"   • {factor}\n"

        analysis += "\n" + "─" * 66 + "\n"
        return analysis

    @staticmethod
    def analyze_refinement_impact(state: Dict[str, Any]) -> str:
        """Analyze refinement decision and its impact.

        Args:
            state: LoanApplicationState as dictionary

        Returns:
            Formatted refinement analysis
        """
        analysis = "\n╔════════════════════════════════════════════════════════════════╗"
        analysis += "\n║            BORDERLINE CASE REFINEMENT ANALYSIS                ║"
        analysis += "\n╚════════════════════════════════════════════════════════════════╝\n"

        if not state.get('llm_decision_refined'):
            return analysis + "No refinement applied.\n"

        llm_analysis = state.get('llm_analysis', {})
        refined = state.get('refined_decision', {})

        # Initial vs Refined
        analysis += "\n🔄 Refinement Applied:\n"
        analysis += "─" * 66 + "\n"
        analysis += f"  Initial Decision: {llm_analysis.get('decision', 'N/A')}"
        analysis += f" (Confidence: {llm_analysis.get('confidence', 0):.1%})\n"
        analysis += f"  Refined Decision: {refined.get('refined_decision', 'N/A')}"
        analysis += f" (Confidence: {refined.get('refined_confidence', 0):.1%})\n"

        # Override decision
        if refined.get('should_override'):
            analysis += f"\n✓ Decision Override Applied\n"
            analysis += f"  Justification: {refined.get('justification', 'N/A')}\n"
        else:
            analysis += f"\n✗ No Override Applied\n"

        analysis += "\n" + "─" * 66 + "\n"
        return analysis


class DecisionExplainer:
    """Utilities for explaining loan decisions with LLM insights."""

    @staticmethod
    def explain_decision(result: Dict[str, Any], state: Optional[Dict[str, Any]] = None) -> str:
        """Generate human-readable explanation of the decision with LLM analysis.

        Args:
            result: Result dictionary from orchestrator
            state: LoanApplicationState (optional) for LLM analysis

        Returns:
            Formatted explanation
        """
        explanation = f"""
╔════════════════════════════════════════════════════════════════╗
║                     LOAN DECISION EXPLANATION                  ║
╚════════════════════════════════════════════════════════════════╝

Application ID: {result.get('application_id', 'N/A')}
Applicant ID: {result.get('applicant_id', 'N/A')}
Decision: {result.get('decision', 'N/A')}
Case ID: {result.get('case_id', 'N/A')}

─────────────────────────────────────────────────────────────────
Decision Metrics:
─────────────────────────────────────────────────────────────────
  Risk Score: {result.get('risk_score', 'N/A'):.2f if result.get('risk_score') else 'N/A'}
  Confidence: {result.get('confidence', 0):.1%}
  Manual Review Required: {result.get('requires_manual_review', False)}

─────────────────────────────────────────────────────────────────
Explanation:
─────────────────────────────────────────────────────────────────
{result.get('explanation', 'No explanation provided')}

─────────────────────────────────────────────────────────────────
Profile Analysis:
─────────────────────────────────────────────────────────────────
"""
        profile = result.get('profile_analysis', {})
        if profile:
            explanation += f"""  Income Stability: {profile.get('income_stability_score', 'N/A'):.2f if profile.get('income_stability_score') else 'N/A'}
  Employment Risk: {profile.get('employment_risk', 'N/A')}
  Completeness: {profile.get('application_completeness_flags', {}).get('completeness_score', 'N/A'):.1%}
"""

        explanation += """─────────────────────────────────────────────────────────────────
Risk Analysis:
─────────────────────────────────────────────────────────────────
"""
        risk = result.get('risk_analysis', {})
        if risk:
            explanation += f"""  DTI Ratio: {risk.get('debt_to_income_ratio', 'N/A'):.2f if risk.get('debt_to_income_ratio') else 'N/A'}
  Credit Risk: {risk.get('credit_score_risk_level', 'N/A')}
  Loan Risk: {risk.get('loan_amount_risk', 'N/A')}
"""
            anomalies = risk.get('anomalies_detected', [])
            if anomalies:
                explanation += f"""  Anomalies Detected:
"""
                for anomaly in anomalies:
                    explanation += f"""    - {anomaly}
"""

        # Add LLM analysis if available
        if state:
            llm_analysis = state.get('llm_analysis')
            if llm_analysis:
                explanation += LLMDecisionAnalyzer.analyze_llm_reasoning(llm_analysis)

            if state.get('llm_decision_refined'):
                explanation += LLMDecisionAnalyzer.analyze_refinement_impact(state)

        explanation += "╚════════════════════════════════════════════════════════════════╝\n"
        return explanation

    @staticmethod
    def print_decision_summary(result: Dict[str, Any]):
        """Print decision summary to console.

        Args:
            result: Result dictionary from orchestrator
        """
        print(DecisionExplainer.explain_decision(result))


class PerformanceDashboard:
    """Performance monitoring and analytics dashboard."""

    @staticmethod
    def create_llm_metrics_dashboard(collector: LLMObservabilityCollector) -> str:
        """Create a performance dashboard for LLM metrics.

        Args:
            collector: LLMObservabilityCollector instance

        Returns:
            Formatted dashboard string
        """
        summary = collector.get_summary()
        metrics = summary["metrics"]
        averages = summary["averages"]

        dashboard = """
╔════════════════════════════════════════════════════════════════╗
║              LLM PERFORMANCE DASHBOARD                         ║
╚════════════════════════════════════════════════════════════════╝

📊 USAGE METRICS:
─────────────────────────────────────────────────────────────────"""

        dashboard += f"""
  Total LLM Calls:        {metrics['total_llm_calls']:>6}
  Total Tokens Used:      {metrics['total_tokens_used']:>6}
  Total Cost:             ${metrics['total_cost']:>6.4f}
  Total Latency:          {metrics['llm_latency_total']:>6.2f}s
"""

        dashboard += """
⚡ PERFORMANCE AVERAGES:
─────────────────────────────────────────────────────────────────"""
        dashboard += f"""
  Avg Latency/Call:       {averages['avg_latency_per_call']:>6.2f}s
  Avg Tokens/Call:        {averages['avg_tokens_per_call']:>6.0f}
  Refinement Rate:        {averages['refinement_rate']:>6.1%}
  Override Rate:          {averages['override_rate']:>6.1%}
"""

        dashboard += """
🎯 DECISION IMPACT:
─────────────────────────────────────────────────────────────────"""
        dashboard += f"""
  Refinements Triggered:  {metrics['refinements_triggered']:>6}
  Decisions Overridden:   {metrics['decisions_overridden']:>6}
  Errors Caught:          {metrics['errors_caught']:>6}
"""

        dashboard += f"""
📈 OVERALL STATS:
─────────────────────────────────────────────────────────────────
  Total Events:           {summary['event_count']:>6}
  Elapsed Time:           {summary['elapsed_time']:>6.2f}s

╚════════════════════════════════════════════════════════════════╝
"""
        return dashboard

    @staticmethod
    def create_cost_analysis(collector: LLMObservabilityCollector) -> str:
        """Create cost analysis report.

        Args:
            collector: LLMObservabilityCollector instance

        Returns:
            Formatted cost analysis
        """
        summary = collector.get_summary()
        metrics = summary["metrics"]
        avg_tokens = summary["averages"]["avg_tokens_per_call"]

        # Estimate based on Claude Opus pricing
        cost_per_mtok_input = 0.003  # $0.003 per 1M input tokens
        cost_per_mtok_output = 0.015  # $0.015 per 1M output tokens

        analysis = """
╔════════════════════════════════════════════════════════════════╗
║              COST ANALYSIS REPORT                              ║
╚════════════════════════════════════════════════════════════════╝

💰 COST BREAKDOWN:
─────────────────────────────────────────────────────────────────"""

        total_cost = metrics['total_cost']
        analysis += f"""
  Total Cost:             ${total_cost:>8.4f}
  Cost per Call:          ${(total_cost / metrics['total_llm_calls'] if metrics['total_llm_calls'] > 0 else 0):>8.4f}
  Cost per Token:         ${(total_cost / metrics['total_tokens_used'] if metrics['total_tokens_used'] > 0 else 0):>8.6f}
"""

        analysis += """
📊 PRICING TIER:
─────────────────────────────────────────────────────────────────
  Model:                  Claude Opus 4.1
  Input Rate:             $0.003 per 1M tokens
  Output Rate:            $0.015 per 1M tokens
"""

        analysis += f"""
✅ SAVINGS ANALYSIS:
─────────────────────────────────────────────────────────────────
  Manual Review Cost:     ${(metrics['total_llm_calls'] * 5):>8.2f} (est.)
  Automated Cost:         ${total_cost:>8.4f}
  Cost Savings:           {((5 * metrics['total_llm_calls'] - total_cost) / (5 * metrics['total_llm_calls']) * 100 if metrics['total_llm_calls'] > 0 else 0):>7.1%}

╚════════════════════════════════════════════════════════════════╝
"""
        return analysis


def print_full_report(
    result: Dict[str, Any],
    execution_trace: List[Dict[str, Any]] = None,
    graph_structure: Dict[str, Any] = None,
    state: Optional[Dict[str, Any]] = None,
    collector: Optional[LLMObservabilityCollector] = None
):
    """Print a full comprehensive report including decision, trace, workflow, and LLM metrics.

    Args:
        result: Result dictionary from orchestrator
        execution_trace: Execution trace (optional)
        graph_structure: Graph structure (optional)
        state: LoanApplicationState (optional) for LLM analysis
        collector: LLMObservabilityCollector (optional) for performance metrics
    """
    # Print decision with LLM analysis
    explanation = DecisionExplainer.explain_decision(result, state)
    print(explanation)

    # Print workflow structure if provided
    if graph_structure:
        WorkflowVisualizer.print_workflow_structure(graph_structure)

    # Print execution trace if provided
    if execution_trace:
        WorkflowVisualizer.print_execution_trace(
            execution_trace,
            application_id=result.get('application_id', 'N/A')
        )

    # Print performance dashboard if collector provided
    if collector:
        dashboard = PerformanceDashboard.create_llm_metrics_dashboard(collector)
        print(dashboard)

        cost_analysis = PerformanceDashboard.create_cost_analysis(collector)
        print(cost_analysis)
