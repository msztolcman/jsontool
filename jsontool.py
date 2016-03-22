#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" jsontool - Perform some actions with json using CLI
    http://msztolcman.github.io/jsontool
    Author: Marcin Sztolcman (marcin@urzenia.net)

    Get help with: jsontool --help
    Information about version: jsontool --version
"""

from __future__ import print_function, unicode_literals

__version__ = '0.2.1'

import re


import argparse
import json
import os.path
import sys
import textwrap


def show_version():
    """
    Show version info and exit.
    :return:
    """

    print('{0}: version {1}'.format(os.path.basename(sys.argv[0]), __version__))
    sys.exit(0)


def build_filters(filter_definitions, invert=False):
    """
    Build function to filter jsons.

    Filter definitions is a list of strings in format: key:value[:modifier]

    :param filter_definitions: list of strings
    :return: function
    """
    filters = []

    if not filter_definitions:
        return lambda item: bool(item)

    value_modifiers = {
        'i': int,
        'f': float,
        's': str,
        'b': bool,
        'l': str.lower,
        'u': str.upper,
        'n': str.lower,
    }
    search_token_modifiers = {
        'n': str.lower,
        'i': int,
        'f': float,
        's': str,
        'b': bool,
    }

    rxp = re.compile(r'''
        ^
            ([^:]+?)            # field
            ([=%^$<>])?         # matcher
            :
            (.*?)               # data
            (?::([ifsblun]))?   # search token modifier
        $
    ''', re.VERBOSE)

    for definition in filter_definitions:
        m = rxp.search(definition)
        if not m:
            raise ValueError("Invalid filter: %s" % definition)

        field, matcher, search_token, value_modifier = m.groups(definition)
        search_token_modifier = search_token_modifiers.get(value_modifier, str)
        value_modifier = value_modifiers.get(value_modifier, str)

        if 0:
            def _debug(data):
                print(field, data[field], search_token, value_modifier(search_token), data)
                return True
            filters.append(_debug)

        search_token = search_token_modifier(search_token)
        if matcher == '%':
            filter_lambda = lambda data: field in data and search_token in value_modifier(data[field])
        elif matcher == '^':
            filter_lambda = lambda data: field in data and value_modifier(data[field]).startswith(search_token)
        elif matcher == '$':
            filter_lambda = lambda data: field in data and value_modifier(data[field]).endswith(search_token)
        elif matcher == '<':
            filter_lambda = lambda data: field in data and search_token > value_modifier(data[field])
        elif matcher == '>':
            filter_lambda = lambda data: field in data and search_token < value_modifier(data[field])
        else:
            filter_lambda = lambda data: field in data and search_token == value_modifier(data[field])

        if invert:
            filters.append(lambda data: not filter_lambda(data))
        else:
            filters.append(filter_lambda)

    def _filter(item):
        return item and all(flt(item) for flt in filters)

    return _filter


def get_printer(mode='auto'):
    """
    Generate printer function.

    :param mode: string: always, never or auto
    :return:
    """

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
    """
    Safely convert data to json (do not throw an exception on fail)

    :param data:
    :return: parsed json
    """

    try:
        return json.loads(data)
    except ValueError:
        pass


def wrap_text(txt):
    """
    Make custom wrapper for passed text.
    Splits given text for lines, and for every line apply custom
    textwrap.TextWrapper settings, then return reformatted string.
    """

    _wrap = textwrap.TextWrapper(
        width = 72,
        expand_tabs = True,
        replace_whitespace = False,
        drop_whitespace = True,
        subsequent_indent = '  ',
    )
    txt = [_wrap.fill(line) for line in txt.splitlines()]
    return "\n".join(txt)


def main():
    """
    Run everything
    """

    epilog = "Argument to --grep option should be in format:\n" \
             "  field:value:modifier\n" \
             "Where: \n" \
             "- \"field\" must be in all JSONs. \n" \
             "- \"value\" is value to search \n" \
             "- \"modifier\" is optional, and say how to treat \"value\": allowed \n" \
             "  options are: s (string - default), b (boolean), i (integer), f (float)"

    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )
    p.add_argument('-f', '--sort-by', type=str,
        help='sort given list of JSONs by this field')
    p.add_argument('-r', '--sort-reversed', action='store_true',
        help='sort in reverse order')
    p.add_argument('-g', '--grep', action='append',
        help='filter list of JSONs using this rules (can be added more then once)')
    p.add_argument('-v', '--invert-match', dest='grep_inverted', action='store_true',
        help='')
    p.add_argument('--version', action='store_true',
        help='show version and exit')
    p.add_argument('--sort-keys', action='store_true',
        help='sort keys in printed JSONs (default: not sorted)')
    p.add_argument('--indent', type=int,
        help='indent JSONs with INDENT spaces')
    p.add_argument('--color', type=str, choices=('auto', 'always', 'never'), default='auto',
        help='manipulate colorizing of JSONs (default: auto)')
    args = p.parse_args()

    if args.version:
        show_version()

    filters = build_filters(args.grep, args.grep_inverted)
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
