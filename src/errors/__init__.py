class SwitcherSlackAppError(Exception):
    """Base class for Switcher Slack App errors"""

class SwitcherContextError(SwitcherSlackAppError):
    """Error raised when Context has missing attributes"""

    def __init__(self, missing: [str]):
        attributes = " - ".join([str(elem) for elem in missing])
        msg = f"Missing [{attributes}]"
        super(SwitcherContextError, self).__init__(msg)

class SwitcherValidationError(SwitcherSlackAppError):
    """Error raised when ticket has issues and cannot be opened"""

    def __init__(self, message: str):
        super(SwitcherValidationError, self).__init__(message)

class SwitcherSlackInstallationError(SwitcherSlackAppError):
    """Error raised when slack installation fails"""

    def __init__(self, message: str):
        super(SwitcherSlackInstallationError, self).__init__(message)