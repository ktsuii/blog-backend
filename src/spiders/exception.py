class ResponseError(Exception):
    """Response status code is not 200."""
    ...


class HtmlSourceError(Exception):
    """Html source changed."""
    ...


class HtmlVerificationError(Exception):
    """HtmlVerification failed."""
    ...
