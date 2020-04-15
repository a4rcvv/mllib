import logging
import os

from slack_log_handler import SlackLogHandler

STOP_LOG = 100


def make_root_logger(console_loglevel: int = logging.DEBUG, file_loglevel: int = STOP_LOG,
                     slack_loglevel: int = STOP_LOG, log_file_path: str = None) -> logging.Logger:
    """Generate the root logger, including Slack log handler.

    Args:
        console_loglevel: the logging level of console handler.
        file_loglevel: the logging level of file log handler.
        slack_loglevel: the logging level of slack log handler.
        log_file_path: the path of log file.

    Returns:
        the root logger

    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s %(module)s::%(funcName)s, line %(lineno)d >> %(message)s"
    )

    if console_loglevel < STOP_LOG:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(console_loglevel)
        root_logger.addHandler(console_handler)

    if log_file_path is not None and file_loglevel < STOP_LOG:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(file_loglevel)
        root_logger.addHandler(file_handler)

    if slack_loglevel < STOP_LOG:
        env_val_name = "WEBHOOK_URL"
        try:
            webhook_url = os.environ[env_val_name]
        except KeyError as e:
            root_logger.error(
                "Environment variable \"{0}\" is not defined, so root logger cannot log to Slack.".format(
                    env_val_name) +
                "Do \"export {0}=(WebHook URL)\" in the terminal or".format(
                    env_val_name) +
                "edit environment variables in Edit Configurations, PyCharm".format(
                    env_val_name))
        else:
            slack_handler = SlackLogHandler(webhook_url)
            slack_handler.setFormatter(formatter)
            slack_handler.setLevel(slack_loglevel)
            root_logger.addHandler(slack_handler)

    return root_logger


def make_child_logger(logger_name: str) -> logging.Logger:
    """Generate a logger, which propagates its logs to the root logger.

    Args:
        logger_name: the name of this logger. "__name__" is recommended.

    Returns:
        logging.Logger

    """
    logger = logging.getLogger(logger_name)
    logger.addHandler(logging.NullHandler())
    logger.setLevel(logging.DEBUG)

    logger.propagate = True

    return logger
