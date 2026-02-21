"""Domain exceptions hierarchy."""
from src.core.constants.errors import ErrorCode


class BaseAPIException(Exception):
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        status_code: int = 500,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class ValidationError(BaseAPIException):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=400,
            details=details,
        )


class NotFoundError(BaseAPIException):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            status_code=404,
            details=details,
        )


class ConfigurationError(BaseAPIException):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.CONFIGURATION_ERROR,
            status_code=500,
            details=details,
        )


class WorkflowError(BaseAPIException):
    def __init__(self, message: str, thread_id: str | None = None, details: dict | None = None) -> None:
        extra = {"thread_id": thread_id} if thread_id else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.WORKFLOW_ERROR,
            status_code=500,
            details={**extra, **(details or {})},
        )


class LLMProviderError(BaseAPIException):
    def __init__(self, message: str, provider: str | None = None, details: dict | None = None) -> None:
        extra = {"provider": provider} if provider else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.LLM_PROVIDER_ERROR,
            status_code=500,
            details={**extra, **(details or {})},
        )
