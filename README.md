# Origins Generators

An Origins generator extracts or derives facts from an existing service or file. Generators will invoked using the [`origins generate <name>`](https://github.com/chop-dbhi/origins/issues/135) subcommand.

To make *calling* a generator consistent, a few simply conventions must be followed:

- All generators **must** write data to standard out
- All generators **must** emit facts in the CSV format and include the header
- All generators **should** use standard POSIX flags (see http://docopt.org for a solid starting point)

For convention, each generator in this respository will be maintained in a `generators/<name>` with the same name it will be invoked with.
