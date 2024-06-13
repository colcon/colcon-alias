# Copyright 2024 Open Source Robotics Foundation, Inc.
# Licensed under the Apache License, Version 2.0

import argparse
import sys
from unittest.mock import Mock
from unittest.mock import patch

from colcon_alias.argument_parser.alias import AliasArgumentParserDecorator
from colcon_alias.verb.alias_invocation import AliasInvocationVerb
import pytest
import yaml


class _RaisingArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        raise sys.exc_info()[1] or Exception(message)


def test_set(fresh_alias_config):
    with fresh_alias_config.open('w') as f:
        yaml.dump({
            'bar': ['foo'],
        }, f)

    extension = AliasArgumentParserDecorator()
    parser = _RaisingArgumentParser()
    decorator = extension.decorate_argument_parser(parser=parser)

    foo_main = Mock()

    subparser = decorator.add_subparsers(
        dest='verb_name')
    foo_parser = subparser.add_parser('foo')
    foo_parser.set_defaults(main=foo_main)

    args, _ = decorator.parse_known_args(['bar'])
    assert isinstance(args.verb_extension, AliasInvocationVerb)
    assert args.main == args.verb_extension.main
    assert args.verb_name == 'bar'

    args = decorator.parse_args(['bar'])
    assert isinstance(args.verb_extension, AliasInvocationVerb)
    assert args.main == args.verb_extension.main
    assert args.verb_name == 'bar'


def test_collision(fresh_alias_config):
    with fresh_alias_config.open('w') as f:
        yaml.dump({
            'foo': ['bar'],
        }, f)

    extension = AliasArgumentParserDecorator()
    parser = _RaisingArgumentParser()
    decorator = extension.decorate_argument_parser(parser=parser)

    foo_main = Mock()

    subparser = decorator.add_subparsers(
        dest='verb_name')
    foo_parser = subparser.add_parser('foo')
    foo_parser.set_defaults(main=foo_main)

    with patch('colcon_alias.argument_parser.alias.logger') as logger:
        args = decorator.parse_args(['foo'])
    assert args.main == foo_main
    assert args.verb_name == 'foo'
    assert logger.warning.call_count == 1


def test_real_verb(fresh_alias_config):
    extension = AliasArgumentParserDecorator()
    parser = _RaisingArgumentParser()
    decorator = extension.decorate_argument_parser(parser=parser)

    foo_main = Mock()

    subparser = decorator.add_subparsers(
        dest='verb_name')
    foo_parser = subparser.add_parser('foo')
    foo_parser.set_defaults(main=foo_main)

    args = decorator.parse_args(['foo'])
    assert args.main == foo_main
    assert args.verb_name == 'foo'


def test_no_verbs(fresh_alias_config):
    with fresh_alias_config.open('w') as f:
        yaml.dump({
            'foo': ['bar'],
        }, f)

    extension = AliasArgumentParserDecorator()
    parser = _RaisingArgumentParser()
    decorator = extension.decorate_argument_parser(parser=parser)

    with pytest.raises(SystemExit, match='^0$'):
        decorator.parse_args(['--help'])
