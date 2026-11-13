"""Workflow visualization and tracing utilities for LangGraph orchestrator."""
import json
from typing import Dict, Any, List
from datetime import datetime
from orchestration.state import LoanApplicationState


class WorkflowVisualizer:
    """Utilities for visualizing and tracing workflow execution."""

    @staticmethod
    def export_to_mermaid(graph_structure: Dict[str, Any]) -> str:
        """Export workflow graph as Mermaid diagram.

        Args:
            graph_structure: Graph structure from orchestrator.get_workflow_graph()

        Returns:
            Mermaid diagram string
        """
        mermaid = "graph TD\n"

        # Add nodes
        node_labels = {
            "applicant_profile": "Profile Analysis",
            "financial_risk": "Financial Risk",
            "loan_decision": "Loan Decision",
            "route_decision": "Route Decision",
            "compliance_action": "Compliance Action",
            "manual_review": "Manual Review",
            "error_handler": "Error Handler",
            "finalize": "Finalize",
            "END": "End"
        }

        for node in graph_structure.get("nodes", []):
            label = node_labels.get(node, node)
            mermaid += f"    {node}[{label}]\n"

        mermaid += "\n"

        # Add edges
        for src, dst in graph_structure.get("edges", []):
            mermaid += f"    {src} --> {dst}\n"

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


class DecisionExplainer:
    """Utilities for explaining loan decisions."""

    @staticmethod
    def explain_decision(result: Dict[str, Any]) -> str:
        """Generate human-readable explanation of the decision.

        Args:
            result: Result dictionary from orchestrator

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
  Risk Score: {result.get('risk_score', 'N/A'):.2f}
  Confidence: {result.get('confidence', 0):.2%}
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
            explanation += f"""  Income Stability: {profile.get('income_stability_score', 'N/A'):.2f}
  Employment Risk: {profile.get('employment_risk', 'N/A')}
  Completeness: {profile.get('application_completeness_flags', {}).get('completeness_score', 'N/A'):.2%}
"""

        explanation += """─────────────────────────────────────────────────────────────────
Risk Analysis:
─────────────────────────────────────────────────────────────────
"""
        risk = result.get('risk_analysis', {})
        if risk:
            explanation += f"""  DTI Ratio: {risk.get('debt_to_income_ratio', 'N/A'):.2f}
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

        explanation += "╚════════════════════════════════════════════════════════════════╝\n"
        return explanation

    @staticmethod
    def print_decision_summary(result: Dict[str, Any]):
        """Print decision summary to console.

        Args:
            result: Result dictionary from orchestrator
        """
        print(DecisionExplainer.explain_decision(result))


def print_full_report(
    result: Dict[str, Any],
    execution_trace: List[Dict[str, Any]] = None,
    graph_structure: Dict[str, Any] = None
):
    """Print a full comprehensive report including decision, trace, and workflow.

    Args:
        result: Result dictionary from orchestrator
        execution_trace: Execution trace (optional)
        graph_structure: Graph structure (optional)
    """
    # Print decision
    DecisionExplainer.print_decision_summary(result)

    # Print workflow structure if provided
    if graph_structure:
        WorkflowVisualizer.print_workflow_structure(graph_structure)

    # Print execution trace if provided
    if execution_trace:
        WorkflowVisualizer.print_execution_trace(
            execution_trace,
            application_id=result.get('application_id', 'N/A')
        )
