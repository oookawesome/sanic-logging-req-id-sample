from sanic.log import logger


class Sample:
    def print_text(self):
        logger.info('test!')
