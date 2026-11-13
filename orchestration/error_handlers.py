"""Error handling utilities for workflow orchestration."""
import logging
from typing import Callable, Any, Dict, Optional
from functools import wraps

logger = logging.getLogger(__name__)


class WorkflowException(Exception):
    """Base exception for workflow errors."""

    def __init__(self, node_name: str, message: str, original_error: Exception = None):
        """Initialize workflow exception.

        Args:
            node_name: Name of the node where error occurred
            message: Error message
            original_error: Original exception that caused this
        """
        self.node_name = node_name
        self.message = message
        self.original_error = original_error
        super().__init__(f"[{node_name}] {message}")


class RetryableException(WorkflowException):
    """Exception that indicates the operation should be retried."""

    pass


class NonRetryableException(WorkflowException):
    """Exception that indicates the operation should not be retried."""

    pass


class ErrorRecoveryStrategy:
    """Strategies for recovering from different types of errors."""

    @staticmethod
    def get_recovery_action(
        error: Exception,
        node_name: str,
        attempt: int,
        max_attempts: int
    ) -> str:
        """Determine the recovery action for an error.

        Args:
            error: The exception that occurred
            node_name: Name of the node
            attempt: Current attempt number
            max_attempts: Maximum number of attempts

        Returns:
            "retry" - retry the operation
            "skip" - skip to next node
            "fail" - fail the entire workflow
        """
        # Non-retryable errors should fail
        if isinstance(error, NonRetryableException):
            logger.error(f"[{node_name}] Non-retryable error: {str(error)}")
            return "fail"

        # If we've exceeded max attempts, fail
        if attempt >= max_attempts:
            logger.error(
                f"[{node_name}] Max attempts ({max_attempts}) exceeded, failing"
            )
            return "fail"

        # Retryable errors should retry
        if isinstance(error, (RetryableException, TimeoutError, ConnectionError)):
            logger.warning(f"[{node_name}] Retryable error on attempt {attempt}, will retry")
            return "retry"

        # Unknown errors - retry a few times before failing
        if attempt < max_attempts:
            logger.warning(f"[{node_name}] Unknown error on attempt {attempt}, will retry")
            return "retry"
        else:
            logger.error(f"[{node_name}] Unknown error exceeded max attempts, failing")
            return "fail"

    @staticmethod
    def get_fallback_value(node_name: str) -> Any:
        """Get a safe fallback value for a failed node.

        Args:
            node_name: Name of the node

        Returns:
            Fallback value for the node
        """
        fallbacks = {
            "applicant_profile": {
                "income_stability_score": 0.5,
                "employment_risk": "Unknown",
                "credit_history_summary": "Unable to retrieve profile",
                "application_completeness_flags": {"all_fields_present": False}
            },
            "financial_risk": {
                "debt_to_income_ratio": 0.5,
                "credit_score_risk_level": "Unknown",
                "loan_amount_risk": "Unknown",
                "anomalies_detected": ["Unable to perform risk analysis"],
                "overall_financial_risk_score": 0.5
            },
            "loan_decision": {
                "classification": "Review",
                "risk_score": 0.5,
                "confidence_level": 0.5,
                "explanation": "Unable to synthesize decision"
            }
        }

        return fallbacks.get(node_name, {})


def handle_node_error(
    node_name: str,
    fallback_on_error: bool = True,
    max_retries: int = 3
) -> Callable:
    """Decorator for handling errors in workflow nodes.

    Args:
        node_name: Name of the node
        fallback_on_error: Whether to return fallback value on error
        max_retries: Maximum number of retries

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            attempt = 0
            last_error = None

            while attempt < max_retries:
                attempt += 1
                try:
                    logger.debug(f"[{node_name}] Executing attempt {attempt}/{max_retries}")
                    result = func(*args, **kwargs)
                    logger.info(f"[{node_name}] ✓ Success on attempt {attempt}")
                    return result

                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"[{node_name}] ✗ Attempt {attempt} failed: {str(e)}"
                    )

                    recovery_action = ErrorRecoveryStrategy.get_recovery_action(
                        e,
                        node_name,
                        attempt,
                        max_retries
                    )

                    if recovery_action == "retry":
                        continue
                    elif recovery_action == "skip":
                        break
                    else:  # "fail"
                        break

            # All attempts exhausted
            logger.error(
                f"[{node_name}] ✗ Failed after {max_retries} attempts. "
                f"Last error: {str(last_error)}"
            )

            if fallback_on_error:
                logger.info(f"[{node_name}] Using fallback value")
                return ErrorRecoveryStrategy.get_fallback_value(node_name)
            else:
                raise last_error

        return wrapper

    return decorator


class ErrorContext:
    """Context manager for handling errors in workflow nodes."""

    def __init__(
        self,
        node_name: str,
        fallback_value: Any = None,
        on_error: Optional[Callable] = None
    ):
        """Initialize error context.

        Args:
            node_name: Name of the node
            fallback_value: Value to return on error
            on_error: Callback function to call on error
        """
        self.node_name = node_name
        self.fallback_value = fallback_value
        self.on_error = on_error
        self.error = None

    def __enter__(self):
        """Enter context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context with error handling."""
        if exc_type is None:
            return False

        self.error = exc_val
        logger.error(
            f"[{self.node_name}] Error: {str(exc_val)}",
            exc_info=(exc_type, exc_val, exc_tb)
        )

        # Call error handler if provided
        if self.on_error:
            self.on_error(exc_val)

        # Suppress exception (return True means exception is handled)
        return True


def validate_state_before_node(required_fields: list) -> Callable:
    """Decorator to validate state before executing a node.

    Args:
        required_fields: List of required fields in state

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(state, *args, **kwargs):
            # Check for required fields
            missing_fields = [field for field in required_fields if not hasattr(state, field) or getattr(state, field) is None]

            if missing_fields:
                logger.warning(
                    f"[{func.__name__}] Missing required fields: {missing_fields}"
                )

            return func(state, *args, **kwargs)

        return wrapper

    return decorator


def log_node_execution(func: Callable) -> Callable:
    """Decorator to log node execution details.

    Args:
        func: Node function

    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(state, *args, **kwargs):
        node_name = func.__name__
        logger.info(f"[{node_name}] ► Starting execution")

        try:
            result = func(state, *args, **kwargs)
            logger.info(f"[{node_name}] ✓ Completed successfully")
            return result
        except Exception as e:
            logger.error(f"[{node_name}] ✗ Failed with error: {str(e)}")
            raise

    return wrapper
