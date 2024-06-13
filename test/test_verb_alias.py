# Copyright 2024 Open Source Robotics Foundation, Inc.
# Licensed under the Apache License, Version 2.0

from unittest.mock import Mock
from unittest.mock import patch

from colcon_alias.verb.alias import AliasVerb
from colcon_core.command import CommandContext
import yaml


def test_add_arguments():
    extension = AliasVerb()
    parser = Mock()
    parser.add_argument = Mock()
    extension.add_arguments(parser=parser)
    assert parser.add_argument.call_count == 2


def test_add(fresh_alias_config):
    extension = AliasVerb()
    context = CommandContext(
        command_name='colcon',
        args=Mock())

    context.args.alias_name = 'foo'
    context.args.command = [
        ['bar', '--baz'],
        ['qux', '--quux'],
    ]

    assert extension.main(context=context) == 0

    assert fresh_alias_config.is_file()
    with fresh_alias_config.open() as f:
        data = yaml.safe_load(f)

    assert data == {
        context.args.alias_name: context.args.command,
    }


def test_add_existing_verb(fresh_alias_config):
    extension = AliasVerb()
    extension.add_arguments(parser=Mock())
    context = CommandContext(
        command_name='colcon',
        args=Mock())

    context.args.alias_name = 'alias'
    context.args.command = [
        ['bar'],
    ]

    assert extension.main(context=context) == 1


def test_remove(fresh_alias_config):
    with fresh_alias_config.open('w') as f:
        yaml.dump({
            'foo': [['bar']],
        }, f)

    extension = AliasVerb()
    context = CommandContext(
        command_name='colcon',
        args=Mock())

    context.args.alias_name = 'foo'
    context.args.command = None

    assert extension.main(context=context) == 0

    with fresh_alias_config.open() as f:
        data = yaml.safe_load(f)

    assert data == {}


def test_remove_not_set(fresh_alias_config):
    extension = AliasVerb()
    context = CommandContext(
        command_name='colcon',
        args=Mock())

    context.args.alias_name = 'foo'
    context.args.command = None

    assert extension.main(context=context) == 0


def test_overwrite(fresh_alias_config):
    with fresh_alias_config.open('w') as f:
        yaml.dump({
            'foo': [['bar']],
        }, f)

    extension = AliasVerb()
    context = CommandContext(
        command_name='colcon',
        args=Mock())

    context.args.alias_name = 'foo'
    context.args.command = [
        ['bar', '--baz'],
        ['qux', '--quux'],
    ]

    assert extension.main(context=context) == 0

    assert fresh_alias_config.is_file()
    with fresh_alias_config.open() as f:
        data = yaml.safe_load(f)

    assert data == {
        context.args.alias_name: context.args.command,
    }


def test_overwrite_same(fresh_alias_config):
    with fresh_alias_config.open('w') as f:
        yaml.dump({
            'foo': [['bar']],
        }, f)

    extension = AliasVerb()
    context = CommandContext(
        command_name='colcon',
        args=Mock())

    context.args.alias_name = 'foo'
    context.args.command = [
        ['bar'],
    ]

    with patch('colcon_alias.config.yaml.dump') as yaml_dump:
        assert extension.main(context=context) == 0

    assert yaml_dump.call_count == 0

    assert fresh_alias_config.is_file()
    with fresh_alias_config.open() as f:
        data = yaml.safe_load(f)

    assert data == {
        context.args.alias_name: context.args.command,
    }
