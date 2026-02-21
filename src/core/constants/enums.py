"""Application enums."""
from enum import StrEnum


class AIProvider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class ThreadStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
