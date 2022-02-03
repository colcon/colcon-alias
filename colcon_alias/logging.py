# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

import logging

from colcon_core.logging import colcon_logger


def _get_effective_log_level():
    for handler in colcon_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            return handler.level
    return logging.WARNING


def configure_filelock_logger():
    """Configure the 'filelock' log level based on colcon's log level."""
    log_level = _get_effective_log_level()
    logging.getLogger('filelock').setLevel(log_level)
