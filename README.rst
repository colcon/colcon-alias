colcon-alias
============

An extension for `colcon-core <https://github.com/colcon/colcon-core>`_ to create and modify command aliases.

Aliases condense any number of colcon command invocations made up of a verb followed by all associated arguments down to another 'alias' verb. When invoking the alias verb, additional arguments can be appended to the original invocations.

An example alias called 'bat', short for 'build and test'::

    $ colcon alias bat --command build --command test
    Registered command list for alias 'bat':
      build
      test
    $ colcon bat --packages-select colcon-alias
    Running command alias: colcon build --packages-select colcon-alias
    ...
    Running command alias: colcon test --packages-select colcon-alias
    ...

Another example, an alias for building specific packages::

    $ colcon alias buildpkg --command build --event-handler console_direct+ --packages-select
    Registered command list for alias 'buildpkg':
      build --event-handler console_direct+ --packages-select
    $ colcon buildpkg colcon-alias
    Running command alias: colcon build --event-handler console_direct+ --packages-select colcon-alias
    ...

A list of currently registered aliases can be found in the colcon help text::

    $ colcon --help
    ...

    colcon aliases:
      bat                   build
                            test
      buildpkg              build --event-handler console_direct+ --packages-select

    ...

Note: When using ``colcon-alias`` with the ``colcon-mixin`` extension, the ``--mixin`` command line argument is applied as an argument to ``--command`` and not used as an actual mixin to the ``alias`` verb.
