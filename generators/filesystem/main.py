#!/usr/bin/env python3
import sys
import os
import csv
import fnmatch
import datetime
from time import strftime

# Minimum possible header.
HEADER = (
    'entity',
    'attribute',
    'value'
)
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

def parse_file(path_id):
    stats = os.stat(path_id)

    # Convert into datetime from timestamp floats
    atime = datetime.datetime.fromtimestamp(stats.st_atime)
    mtime = datetime.datetime.fromtimestamp(stats.st_mtime)

    if hasattr(stats, 'st_birthtime'):
        create_time = stats.st_birthtime
    else:
        create_time = stats.st_ctime

    ctime = datetime.datetime.fromtimestamp(create_time)

    return {
        'id': path_id,
        'mode': stats.st_mode,
        'uid': stats.st_uid,
        'gid': stats.st_gid,
        'size': stats.st_size,
        'accessed': atime.strftime(DATETIME_FORMAT),
        'modified': mtime.strftime(DATETIME_FORMAT),
        'created': ctime.strftime(DATETIME_FORMAT),
    }

def parse_directory(dir_path, path):
    path_id = os.path.relpath(path, dir_path)

    return {
        'id': path_id,
    }

def generate(path, pattern, hidden, depth):
    # Creating a CSV writer that feeds to stdout.
    w = csv.writer(sys.stdout)

    # Write the header to start.
    w.writerow(HEADER)


    for root, dirs, names in os.walk(path):
        if depth is not None:
            curpath = os.path.relpath(root, base_path)
            if curpath == '.':
                depth = 0
            else:
                depth = len(curpath.split(os.path.sep))

            # Remove all subdirectories from traversal once the
            # desired depth has been reached. Note a `break` does
            # not work since this would stop processing sibling
            # directories as well.
            for dirname in dirs[:]:
                if depth >= self.depth:
                    dirs.pop()
                elif not hidden and dirname.startswith('.'):
                    dirs.pop()

        directory = parse_directory(path, root)

        for i, f in enumerate(fnmatch.filter(names, pattern)):
            if not hidden and f.startswith('.'):
                continue
            file = parse_file(os.path.abspath(os.path.join(
                path,
                directory['id'],
                f
            )))

            for key, value in file.items():
                if directory['id'] == '.':
                   entity = f
                else:
                   entity = os.path.join(directory['id'], f)

                w.writerow ([
                    entity,
                    key,
                    value
                ])

    # Flush the remaining bits.
    sys.stdout.flush()

def main():
    usage = """Origins Filesystem Generator.

    Usage:
        filesystem <path> [--pattern=<pattern>] [--hidden=<hidden>] [--depth=<depth>]

    Options:
        -h --help  Show usage info.
        --pattern=<pattern> The filename pattern to collect facts from.
        --hidden=<hidden> If true, hideen files and directories will be included.
        --depth=<depth> The desired depth to recurse into the directory tree.
    """ #noqa

    from docopt import docopt

    # Trim './main.py filesystem' from the line.
    args = docopt(usage, version='0.1')

    # Defaults
    pattern = '*'
    hidden = False
    depth = None

    # Collect arg values
    dir_path = os.path.join(os.getcwd(), args['<path>'])
    if args['--pattern'] is not None:
        pattern = args['--pattern']

    if args['--hidden'] is not None:
        hidden = args['--hidden']

    if args['--depth'] is not None:
        depth = args['--depth']

    # No need to validate input because docopt makes sure all arguments are given
    generate(dir_path, pattern, hidden, depth)

if __name__ == '__main__':
    main()
