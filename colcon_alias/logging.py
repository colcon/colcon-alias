# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

import logging

from colcon_core.logging import colcon_logger
from colcon_core.logging import get_effective_console_level


def configure_filelock_logger():
    """Configure the 'filelock' log level based on colcon's log level."""
    log_level = get_effective_console_level(colcon_logger)
    logging.getLogger('filelock').setLevel(log_level)
