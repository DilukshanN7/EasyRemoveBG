class EasyRemoveBGError(Exception):
    """Base error for user-facing failures."""


class DependencyError(EasyRemoveBGError):
    """Raised when an optional runtime dependency is missing."""
