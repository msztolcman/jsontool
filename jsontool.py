#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import argparse
import json
import sys

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import get_formatter_by_name

    lexer = get_lexer_by_name('json')
    formatter = get_formatter_by_name('terminal256')

    def print_colorized(data, dst=sys.stdout):
        if hasattr(dst, 'isatty') and dst.isatty():
            print(highlight(data, lexer, formatter), end='', file=dst)
        else:
            print(data, file=dst)
except ImportError as e:
    def print_colorized(data, dst=sys.stdout):
        print(data, file=dst)


def build_filters(filter_definitions):
    filters = []

    if not filter_definitions:
        return lambda item: bool(item)

    for definition in filter_definitions:
        key, value = definition.split(':', 1)
        filters.append(lambda data: key in data and data[key] == value)

    def _filter(item):
        return item and all(flt(item) for flt in filters)

    return _filter


def json_loads(data):
    try:
        return json.loads(data)
    except ValueError:
        pass


p = argparse.ArgumentParser()
p.add_argument('-f', '--field', type=str)
p.add_argument('-g', '--grep', action='append')
# p.add_argument('-l', '--highlight', type=str)
args = p.parse_args()

filters = build_filters(args.grep)

data = map(json_loads, sys.stdin)
data = filter(filters, data)
data.sort(key=lambda item: item[args.field])

for line in data:
    line = json.dumps(line)
    print_colorized(line)