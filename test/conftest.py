# Copyright 2024 Open Source Robotics Foundation, Inc.
# Licensed under the Apache License, Version 2.0

from pathlib import Path
from unittest.mock import patch

from colcon_alias import CONFIG_NAME
import pytest


@pytest.fixture
def fresh_alias_config(tmpdir):
    tmpdir = Path(tmpdir)
    with patch('colcon_alias.config.get_config_path', return_value=tmpdir):
        yield tmpdir / CONFIG_NAME
