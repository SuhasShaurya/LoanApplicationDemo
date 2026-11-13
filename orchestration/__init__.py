"""Orchestration module for loan approval system."""

from config.settings import settings

# Try to import orchestrators in order of preference
LoanOrchestrator = None
create_orchestrator = None
EnhancedLoanOrchestrator = None
create_enhanced_orchestrator = None

# Try enhanced orchestrator first
try:
    from .langgraph_orchestrator import EnhancedLoanOrchestrator, create_enhanced_orchestrator
except ImportError:
    EnhancedLoanOrchestrator = None
    create_enhanced_orchestrator = None

# Try standard LangGraph orchestrator
try:
    from .orchestrator import LoanOrchestrator, create_orchestrator
except ImportError:
    LoanOrchestrator = None
    create_orchestrator = None

# Import simple orchestrator (always available)
from .simple_orchestrator import SimpleOrchestrator, create_simple_orchestrator
from .state import LoanApplicationState

# Import utilities
from .workflow_viz import WorkflowVisualizer, DecisionExplainer, print_full_report
from .error_handlers import WorkflowException, RetryableException, NonRetryableException


def get_default_orchestrator():
    """Get the default orchestrator based on configuration.

    Returns the enhanced orchestrator by default, with fallback chain:
    1. Enhanced LangGraph orchestrator (if available and configured)
    2. Standard LangGraph orchestrator (if available)
    3. Simple orchestrator (always available)
    """
    if getattr(settings, 'USE_ENHANCED_ORCHESTRATOR', True):
        if create_enhanced_orchestrator:
            return create_enhanced_orchestrator(
                max_retries=getattr(settings, 'MAX_RETRIES', 3),
                retry_delay=getattr(settings, 'RETRY_DELAY', 1.0)
            )

    if create_orchestrator:
        return create_orchestrator()

    return create_simple_orchestrator()


# Build exports list
__all__ = [
    "SimpleOrchestrator",
    "create_simple_orchestrator",
    "LoanApplicationState",
    "WorkflowVisualizer",
    "DecisionExplainer",
    "print_full_report",
    "WorkflowException",
    "RetryableException",
    "NonRetryableException",
    "get_default_orchestrator",
]

# Add optional exports
if LoanOrchestrator:
    __all__.extend(["LoanOrchestrator", "create_orchestrator"])

if EnhancedLoanOrchestrator:
    __all__.extend(["EnhancedLoanOrchestrator", "create_enhanced_orchestrator"])
