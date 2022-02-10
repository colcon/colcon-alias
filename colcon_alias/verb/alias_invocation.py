# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

from colcon_core.argument_parser import SuppressUsageOutput
from colcon_core.command import add_parser_arguments
from colcon_core.command import add_parsers_without_arguments
from colcon_core.command import CommandContext
from colcon_core.command import create_parser
from colcon_core.command import create_subparser
from colcon_core.command import verb_main
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.verb import get_verb_extensions
from colcon_core.verb import VerbExtensionPoint


class AliasInvocationVerb(VerbExtensionPoint):
    """Invokes a command alias."""

    def __init__(self, commands):  # noqa: D107
        super().__init__()
        satisfies_version(VerbExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')
        self._commands = commands

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '-h', '--help', action='help',
            help='show this help message and exit')
        parser.add_argument(
            'additional_args', nargs='*', type=str.lstrip, default=[],
            help='Additional arguments to pass to each command')

    def main(self, *, context):  # noqa: D102
        parser = create_parser('colcon_core.environment_variable')
        verb_extensions = get_verb_extensions()
        subparser = create_subparser(
            parser, context.command_name, verb_extensions,
            attribute='verb_name')
        verb_parsers = add_parsers_without_arguments(
            parser, subparser, verb_extensions, attribute='verb_name')

        added_verbs = set()

        for command in self._commands:
            argv = command + context.args.additional_args
            print(
                'Running command alias: {} {}'.format(
                    context.command_name, ' '.join(argv)))

            with SuppressUsageOutput([parser] + list(verb_parsers.values())):
                known_args, _ = parser.parse_known_args(args=argv)
            if getattr(known_args, 'verb_name', None):
                if known_args.verb_name not in added_verbs:
                    add_parser_arguments(
                        known_args.verb_parser, known_args.verb_extension)
                    added_verbs.add(known_args.verb_name)

            args = parser.parse_args(args=argv)
            alias_context = CommandContext(
                command_name=context.command_name, args=args)

            rc = verb_main(alias_context, colcon_logger)
            if rc:
                return rc
