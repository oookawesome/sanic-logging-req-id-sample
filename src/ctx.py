from _contextvars import ContextVar


class Ctx:
    request_id = ContextVar('request_id', default='00000000')
