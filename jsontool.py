#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" jsontool - Perform some actions with json using CLI
    http://github.com/mysz/jsontool
    Author: Marcin Sztolcman (marcin@urzenia.net)

    Get help with: jsontool --help
    Information about version: jsontool --version
"""

from __future__ import print_function, unicode_literals

__version__ = '0.1.0'


import argparse
import json
import os.path
import sys


def show_version():
    """ Show version info and exit.
    """

    print('{0}: version {1}'.format(os.path.basename(sys.argv[0]), __version__))
    sys.exit(0)


def build_filters(filter_definitions):
    filters = []

    if not filter_definitions:
        return lambda item: bool(item)

    modifiers = {
        'i': int,
        'f': float,
        's': str,
        'b': bool,
    }
    for definition in filter_definitions:
        try:
            key, value, modifier = definition.split(':', 2)
            modifier = modifiers.get(modifier, None)
        except ValueError:
            key, value = definition.split(':', 1)
            modifier = str

        if not modifier:
            modifier = lambda item: item
        filters.append(lambda data: key in data and data[key] == modifier(value))

    def _filter(item):
        return item and all(flt(item) for flt in filters)

    return _filter


def get_printer(mode):
    def printer(data):
        print(data)

    if mode in ('auto', 'always'):
        try:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import get_formatter_by_name

            if mode == 'always' or sys.stdout.isatty():
                lexer = get_lexer_by_name('json')
                formatter = get_formatter_by_name('terminal256')

                def printer(data):
                    print(highlight(data, lexer, formatter), end='', file=sys.stdout)
        except ImportError as e:
            if mode == 'always':
                import warnings
                warnings.warn('No pygments module available, cannot colorize output')

    return printer

def json_loads(data):
    try:
        return json.loads(data)
    except ValueError:
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--sort-by', type=str)
    p.add_argument('-r', '--sort-reversed', action='store_true')
    p.add_argument('-g', '--grep', action='append')
    p.add_argument('-v', '--version', action='store_true')
    p.add_argument('--sort-keys', action='store_true')
    p.add_argument('--indent', type=int)
    p.add_argument('--color', type=str, choices=('auto', 'always', 'never'), default='auto')
    args = p.parse_args()

    if args.version:
        show_version()

    filters = build_filters(args.grep)
    printer = get_printer(args.color)

    data = map(json_loads, sys.stdin)
    data = filter(filters, data)

    if args.sort_by:
        data.sort(key=lambda item: item[args.sort_by], reverse=args.sort_reversed)

    for line in data:
        line = json.dumps(line, sort_keys=args.sort_keys, indent=args.indent)
        printer(line)


if __name__ == '__main__':
    main()
