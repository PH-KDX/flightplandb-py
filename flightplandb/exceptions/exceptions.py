class BaseErrorHandler(Exception):
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
