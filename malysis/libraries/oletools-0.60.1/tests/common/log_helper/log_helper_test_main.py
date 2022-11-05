""" Test log_helpers """

import sys
import logging
from tests.common.log_helper import log_helper_test_imported
from oletools.common.log_helper import log_helper

DEBUG_MESSAGE = 'main: debug log'
INFO_MESSAGE = 'main: info log'
WARNING_MESSAGE = 'main: warning log'
ERROR_MESSAGE = 'main: error log'
CRITICAL_MESSAGE = 'main: critical log'
RESULT_MESSAGE = 'main: result log'
RESULT_TYPE = 'main: result'

logger = log_helper.get_or_create_silent_logger('test_main')


def enable_logging():
    """Enable logging if imported by third party modules."""
    logger.setLevel(log_helper.NOTSET)
    log_helper_test_imported.enable_logging()


def main(args):
    """
    Try to cover possible logging scenarios. For each scenario covered, here's the expected args and outcome:
    - Log without enabling: ['<level>']
        * logging when being imported - should never print
    - Log as JSON without enabling: ['as-json', '<level>']
        * logging as JSON when being imported - should never print
    - Enable and log: ['enable', '<level>']
        * logging when being run as script - should log messages
    - Enable and log as JSON: ['as-json', 'enable', '<level>']
        * logging as JSON when being run as script - should log messages as JSON
    - Enable, log as JSON and throw: ['enable', 'as-json', 'throw', '<level>']
        * should produce JSON-compatible output, even after an unhandled exception
    """

    # the level should always be the last argument passed
    level = args[-1]
    use_json = 'as-json' in args
    throw = 'throw' in args
    percent_autoformat = '%-autoformat' in args

    log_helper_test_imported.logger.setLevel(logging.ERROR)

    if 'enable' in args:
        log_helper.enable_logging(use_json, level, stream=sys.stdout)

    do_log(percent_autoformat)

    if throw:
        raise Exception('An exception occurred before ending the logging')

    log_helper.end_logging()


def do_log(percent_autoformat=False):
    if percent_autoformat:
        logger.info('The %s is %d.', 'answer', 47)

    logger.debug(DEBUG_MESSAGE)
    logger.info(INFO_MESSAGE)
    logger.warning(WARNING_MESSAGE)
    logger.error(ERROR_MESSAGE)
    logger.critical(CRITICAL_MESSAGE)
    logger.info(RESULT_MESSAGE, type=RESULT_TYPE)
    log_helper_test_imported.log()


if __name__ == '__main__':
    main(sys.argv[1:])
