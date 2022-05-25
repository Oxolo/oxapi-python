"""Module that contain all the custom python exceptions for managing OxAPI
errors."""


class OxAPIError(Exception):
    """Generic OxAPI exception."""

    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        super(OxAPIError, self).__init__(message)
        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}

    def __str__(self):
        msg = self._message or "<empty message>"
        return "Error code: {0}, Error message: {1}".format(self.http_status, msg)


class InvalidAPIKeyException(OxAPIError):
    pass


class NotFoundException(OxAPIError):
    pass


class NotAllowedException(OxAPIError):
    pass


class ModelNotFoundException(Exception):
    pass
