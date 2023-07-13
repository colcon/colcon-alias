# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

import sys

from colcon_alias.config import update_config
from colcon_core.plugin_system import satisfies_version
from colcon_core.verb import get_verb_extensions
from colcon_core.verb import VerbExtensionPoint


class AliasVerb(VerbExtensionPoint):
    """Create and modify command aliases."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(VerbExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            'alias_name',
            help='Name of the alias verb to create, modify, or remove')
        parser.add_argument(
            '--command', nargs='+', action='append',
            help='Command(s) to be invoked when the alias is used',
            metavar=('VERB', 'ARGUMENTS'))

    def main(self, *, context):  # noqa: D102
        if (
            context.args.command and
            context.args.alias_name in get_verb_extensions()
        ):
            print(
                'There is already a verb with the name '
                "'{context.args.alias_name}'".format_map(locals()),
                file=sys.stderr)
            return 1
        update_config(context.args.alias_name, context.args.command)
        if not context.args.command:
            print(f"Alias '{context.args.alias_name}' has been removed.")
        else:
            print(
                'Registered command list for alias '
                f"'{context.args.alias_name}':")
            for command in context.args.command:
                print(f"  {' '.join(command)}")
