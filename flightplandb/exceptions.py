class BaseErrorHandler(Exception):
    __module__ = "Exception"

    def __init__(self, status_code, message=None):
        self.status_code = status_code
        self.message = message


class BadRequestException(BaseErrorHandler):
    pass


class ForbiddenException(BaseErrorHandler):
    pass


class NotFoundException(BaseErrorHandler):
    pass


class InternalServerException(BaseErrorHandler):
    pass


def status_handler(status_code, ignore_statuses=None):
    if status_code not in ignore_statuses and status_code >= 400:
        if status_code == 400:
            raise BadRequestException(
                "The request could not be understood by \
                the server due to malformed syntax."
            )
        elif status_code == 403:
            raise ForbiddenException(
                "The server understood the request, \
                but is refusing to fulfill it."
            )
        elif status_code == 404:
            raise NotFoundException(
                "The server has not found anything matching the Request-URI."
            )
        elif status_code == 500:
            raise InternalServerException(
                "The server encountered an unexpected condition \
                which prevented it from fulfilling the request."
            )
        else:
            raise BaseErrorHandler(
                status_code,
                "Unknown Error Occurred."
            )
