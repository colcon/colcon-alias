# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

from colcon_alias.config import get_config
from colcon_alias.verb.alias_invocation import AliasInvocationVerb
from colcon_core.argument_parser import ArgumentParserDecorator
from colcon_core.argument_parser import ArgumentParserDecoratorExtensionPoint
from colcon_core.plugin_system import satisfies_version


class AliasArgumentParserDecorator(ArgumentParserDecoratorExtensionPoint):
    """Add command aliases verbs to the argument parser."""

    # Because this parser adds subparsers, it needs to be added after
    # other decorators like colcon-defaults that track them
    PRIORITY = 50

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            ArgumentParserDecoratorExtensionPoint.EXTENSION_POINT_VERSION,
            '^1.0')

    def decorate_argument_parser(self, *, parser):  # noqa: D102
        return AliasArgumentDecorator(parser)


class AliasArgumentDecorator(ArgumentParserDecorator):
    """Add command aliases verbs to the argument parser."""

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs, _subparser=None, _done=False)

    def add_subparsers(self, *args, **kwargs):  # noqa: D102
        self._subparser = super().add_subparsers(*args, **kwargs)
        return self._subparser

    def parse_args(self, *args, **kwargs):  # noqa: D102
        self._add_aliases()
        return self._parser.parse_args(*args, **kwargs)

    def parse_known_args(self, *args, **kwargs):  # noqa: D102
        self._add_aliases()
        return self._parser.parse_known_args(*args, **kwargs)

    def _add_aliases(self):
        if self._done:
            return

        add_args_now = False
        if not self._subparser:
            add_args_now = True
            self.add_subparsers(
                title='colcon verbs', dest='verb_name')

        config = get_config()
        if not config:
            return

        aliases = []
        for alias, commands in config.items():
            command_strings = [' '.join(c) for c in commands]

            commands_ind = ('\n' + ' ' * 24).join(command_strings)
            aliases.append('  {alias:21} {commands_ind}'.format_map(locals()))

            commands_ind = '\n  '.join(command_strings)
            alias_parser = self._subparser.add_parser(
                alias, add_help=False,
                description='This is an alias for the following command(s):\n'
                            '  {commands_ind}'.format_map(locals()),
                formatter_class=self._parser.formatter_class)

            extension = AliasInvocationVerb(commands)
            alias_parser.set_defaults(
                verb_parser=alias_parser, verb_extension=extension,
                main=extension.main)

            if add_args_now:
                extension.add_arguments(parser=alias_parser)

        epilog = self._parser.prog + ' aliases:\n' + '\n'.join(aliases)
        if self._parser.epilog:
            self._parser.epilog = epilog + '\n\n' + self._parser.epilog
        else:
            self._parser.epilog = epilog

        self._done = True
