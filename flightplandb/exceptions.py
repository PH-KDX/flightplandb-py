class BaseErrorHandler(Exception):
    """Base exception. The other exceptions all inherit from
    this one, but this exception will be raised directly if
    no others match the returned HTTP status code.

    Attributes
    ----------
    status_code
        Status code of the error
    message
        Description of the error
    """

    def __init__(self, status_code=None, message=None):
        self.status_code = status_code
        self.message = message
        super().__init__(self.status_code, self.message)


class BadRequestException(BaseErrorHandler):
    """An incorrect request was made to the server.
    Raised for an HTTP status code 400.

    Attributes
    ----------
    status_code
        Not used
    message
        A verbose description of this error.
    """
    pass


class UnauthorizedException(BaseErrorHandler):
    """You are incorrectly authorised and may not make this request.
    Raised for an HTTP status code 401.

    Attributes
    ----------
    status_code
        Not used
    message
        A verbose description of this error.
    """
    pass


class ForbiddenException(BaseErrorHandler):
    """The server refuses to fulfill this request,
    for instance due to insufficient authentication.
    Raised for an HTTP status code 403.

    Attributes
    ----------
    status_code
        Not used
    message
        A verbose description of this error.
    """
    pass


class NotFoundException(BaseErrorHandler):
    """The server couldn't find a resource matching the request.
    Raised for an HTTP status code 404.

    Attributes
    ----------
    status_code
        Not used
    message
        A verbose description of this error.
    """
    pass


class InternalServerException(BaseErrorHandler):
    """Something unspecified went wrong with the server.
    Raised for an HTTP status code 500.

    Attributes
    ----------
    status_code
        Not used
    message
        A verbose description of this error.
    """
    pass


def status_handler(status_code, ignore_statuses=None):
    if status_code not in ignore_statuses and status_code >= 400:
        if status_code == 400:
            raise BadRequestException(
                status_code=status_code,
                message="The request could not be understood by "
                "the server due to malformed syntax."
            )
        if status_code == 401:
            raise UnauthorizedException(
                status_code=status_code,
                message="You are incorrectly authorised and "
                "may not make this request."
            )
        elif status_code == 403:
            raise ForbiddenException(
                status_code=status_code,
                message="The server understood the request, "
                "but is refusing to fulfill it."
            )
        elif status_code == 404:
            raise NotFoundException(
                status_code=status_code,
                message="The server has not found anything "
                "matching the Request-URI."
            )
        elif status_code == 500:
            raise InternalServerException(
                status_code=status_code,
                message="The server encountered an unexpected condition "
                "which prevented it from fulfilling the request."
            )
        else:
            raise BaseErrorHandler(
                status_code=status_code,
                message="Unknown Error Occurred."
            )
