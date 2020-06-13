class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class PostGetErrors(Error):
    errors = {
        204: "No content",
        400: "Bad request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not found",
        409: "Conflict",
        415: "Unsupported media type",
        422: "Unprocessable entity",
        429: "Too many Requests",
        500: "Internal Server Error"
    }

    def __init__(self, status_code, message):
        self.expression = status_code
        self.message = str(status_code) + ": "+self.errors.get(status_code, "Unknown issue") + " " + message
