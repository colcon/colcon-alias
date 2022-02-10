# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

from colcon_alias.config import update_config
from colcon_core.plugin_system import satisfies_version
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
        update_config(context.args.alias_name, context.args.command)
        if not context.args.command:
            print(
                "Alias '{context.args.alias_name}' has "
                'been removed.'.format_map(locals()))
        else:
            print(
                'Registered command list for alias '
                "'{context.args.alias_name}':".format_map(locals()))
            for command in context.args.command:
                print('  {}'.format(' '.join(command)))
