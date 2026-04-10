class EasyRemoveBGError(Exception):
    """Base error for user-facing failures."""


class DependencyError(EasyRemoveBGError):
    """Raised when an optional runtime dependency is missing."""


class UnsupportedPlatformError(EasyRemoveBGError):
    """Raised when a platform-specific operation is not supported."""
