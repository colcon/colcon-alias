# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

from colcon_alias import CONFIG_NAME
from colcon_alias.logging import configure_filelock_logger
from colcon_core.location import get_config_path
import filelock
import yaml


def get_config():
    """Get the global colcon-alias configuration."""
    configure_filelock_logger()

    config_path = get_config_path()
    config_path.mkdir(parents=True, exist_ok=True)
    config_file = config_path / CONFIG_NAME
    lock_file = config_path / '.{}.lock'.format(CONFIG_NAME)
    try:
        with filelock.FileLock(lock_file, timeout=5):
            with config_file.open() as f:
                return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def update_config(alias_name, commands):
    """Update the global colcon-alias configuration."""
    configure_filelock_logger()

    config_path = get_config_path()
    config_path.mkdir(parents=True, exist_ok=True)
    config_file = config_path / CONFIG_NAME
    lock_file = config_path / '.{}.lock'.format(CONFIG_NAME)
    with filelock.FileLock(lock_file, timeout=5):
        with config_file.open('a+') as f:
            f.seek(0)
            config = yaml.safe_load(f) or {}
            if not commands:
                if alias_name in config:
                    del config[alias_name]
                else:
                    return
            elif config.get(alias_name, []) == commands:
                return
            else:
                config[alias_name] = commands
            f.seek(0)
            f.truncate()
            yaml.dump(config, f, default_style="'")
