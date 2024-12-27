# import APIException
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class BaseException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail=None, code=None):
        super().__init__(detail=detail, code=code)
        self.detail = detail
        self.status_code = code


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")
    default_code = "invalid"

    def __init__(self, missing_fields=None, detail=None, code=None):
        if missing_fields is not None:
            detail = {"error": "Validation Error", "missing_fields": missing_fields}
        super().__init__(detail, code)


class ParseError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Malformed request.")
    default_code = "parse_error"


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Bad Request.")
    default_code = "bad_request"


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Incorrect authentication credentials.")
    default_code = "authentication_failed"


class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Authentication credentials were not provided.")
    default_code = "not_authenticated"


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("You do not have permission to perform this action.")
    default_code = "permission_denied"


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Not found.")
    default_code = "not_found"


class MethodNotAllowed(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = _('Method "{method}" not allowed.')
    default_code = "method_not_allowed"
