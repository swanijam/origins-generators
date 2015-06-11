# Origins Generators

An Origins generator extracts or derives facts from an existing service or file. Generators will invoked using the [`origins generate <name>`](https://github.com/chop-dbhi/origins/issues/135) subcommand.

To make *calling* a generator consistent, a few simply conventions must be followed:

- All generators **must** write data to standard out
- All generators **must** emit facts in the CSV format and include the header
- All generators **should** use standard POSIX flags (see http://docopt.org for a solid starting point)

For convention, each generator in this respository will be maintained in a `generators/<name>` with the same name it will be invoked with.

Since generators can implemented using any technology, a Dockerfile should be included that encapsulates the program to make it simpler to call without needing to install any dependencies.

## Example

This is a trivial, but valid example of what a program could look like.

```python
#!/usr/bin/env python

import os
import sys
import csv
import time


# Minimum possible header.
HEADER = (
    'entity',
    'attribute',
    'value',
)


def main(root):
    "Outputs last modified times of the files in the specified directory."
    # Creating a CSV writer that feeds to stdout.
    w = csv.writer(sys.stdout)
    
    # Write the header to start.
    w.writerow(HEADER)
    
    # Generate 100 uninteresting facts.
    for path in os.listdir(root):
        w.writerow((
            path,
            'last_modified',
            time.ctime(os.path.getmtime(path)),
        ))

    # Flush the remaining bits.
    sys.stdout.flush()


if __name__ == '__main__':
    main(*sys.argv[1:])
```
