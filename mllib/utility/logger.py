import inspect
import logging
from urllib.error import HTTPError

import slackweb


class Logger:
    """The class to wrap "logging" in standard library and "slackweb".

    """

    # logging.CRITICAL is defined as 50, which is the highest value defined in logging.
    # I will use 100 to show that a logger have not to log.
    STOP_LOG = 100

    # These values are from logger.py. I defined them here to use them without importing "logging"
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    _slack_webhook_url: str = None
    _slack: slackweb.Slack = None

    @staticmethod
    def set_webhook(webhook_url: str) -> None:
        """Set the Webhook URL for Slack. Class method.

        Args:
            webhook_url: Webhook URL

        """
        Logger._slack_webhook_url = webhook_url
        Logger._slack = slackweb.Slack(webhook_url)

    def __init__(self, logger_name: str, console_loglevel: int = STOP_LOG, file_loglevel: int = STOP_LOG,
                 slack_loglevel: int = STOP_LOG, log_file_path: str = None):
        """

        Args:
            logger_name:
            console_loglevel:
            file_loglevel:
            slack_loglevel:
            log_file_path:
        """
        self.logger = logging.getLogger(logger_name)
        self.slack_loglevel = slack_loglevel

        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(levelname)s %(asctime)s %(message)s"
        )

        if console_loglevel < Logger.STOP_LOG:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(console_loglevel)
            self.logger.addHandler(console_handler)

        if log_file_path is not None and file_loglevel < Logger.STOP_LOG:
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(file_loglevel)
            self.logger.addHandler(file_handler)

    def _log_to_slack(self, loglevel: int, message: str) -> None:
        """Send a log message to Slack.

        Args:
            loglevel: Level of logging like "logger.CRITICAL"
            message: log message

        """

        if self.slack_loglevel <= loglevel:
            if Logger._slack is None:
                self.error("Webhook url is not defined. You must do Logger.set_webhook(url).", False)
            else:
                try:
                    Logger._slack.notify(text=message)
                except HTTPError as e:
                    self.error("Failed to log to slack. HTTP Status is: " + e.reason, False)

    @staticmethod
    def _make_message(original_message: str) -> str:
        framerecords = inspect.stack()
        framerecord = framerecords[2]
        file_name = framerecord[1]
        line_number = framerecord[2]
        func_name = framerecord[3]

        return "{0}::{1}, line {2} >> {3}".format(file_name, func_name, line_number, original_message)

    def debug(self, message: str, should_log_slack: bool = True):
        message = Logger._make_message(message)
        self.logger.debug(message)
        if should_log_slack:
            self._log_to_slack(logging.DEBUG, "DEBUG " + message)

    def info(self, message: str, should_log_slack: bool = True):
        message = Logger._make_message(message)
        self.logger.info(message)
        if should_log_slack:
            self._log_to_slack(logging.INFO, "INFO " + message)

    def warning(self, message: str, should_log_slack: bool = True):
        message = Logger._make_message(message)
        self.logger.warning(message)
        if should_log_slack:
            self._log_to_slack(logging.WARNING, "WARNING " + message)

    def error(self, message: str, should_log_slack: bool = True):
        message = Logger._make_message(message)
        self.logger.error(message)
        if should_log_slack:
            self._log_to_slack(logging.ERROR, "ERROR " + message)

    def critical(self, message: str, should_log_slack: bool = True):
        message = Logger._make_message(message)
        self.logger.critical(message)
        if should_log_slack:
            self._log_to_slack(logging.CRITICAL, "CRITICAL " + message)
