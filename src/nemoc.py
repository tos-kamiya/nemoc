#!/usr/bin/env python
#coding: utf-8

r"""
nomoc, a command-line rendering tool for NEMO template
"""

__author__ = "Toshihiro Kamiya <kamiya@mbj.nifty.com>"
__status__ = "alpha"
__version__ = "0.1"
__date__ = "14 September 2012"

from nemo.parser import NemoParser
from mako.template import Template


def render(s, params={}):
    r"""
    render(s, params={})
    
    Returns a rendering result of template s with parameters params.
    The result string is an unicode string.
    
    >>> render('%img src="images/mrfoobar.jpg" alt="Mr. FooBar"')
    u'\n<img src="images/mrfoobar.jpg" alt="Mr. FooBar" />'
    """

    nemo = NemoParser(debug=False).parse
    return Template(s, preprocessor=nemo).render_unicode(**params)


USAGE = """
Usage: nemoc [-o <rendered.html>] [<template.nemo>] [--<key>=<value>...]
  Renders a given nemo template.
"""[1:-1]


def _parse_args(args):
    OPTION_O = '-o'

    if args and args[0] in ('-h', '--help'):
        print(USAGE)
        raise SystemExit(0)

    args = args[:]
    src = None
    dest = None
    params = {}
    for i, a in enumerate(args):
        if a.startswith("-"):
            if a == OPTION_O:
                args[i + 1] = OPTION_O + args[i + 1]
            elif a.startswith(OPTION_O):
                assert dest is None
                dest = a[len(OPTION_O):]
            elif a.startswith("--"):
                kv = a[2:].split("=")
                if len(kv) != 2:
                    raise SystemExit("invalid parameter. expected '<key>=<value>'")
                if kv[0] in params:
                    raise SystemExit("confliction of parameter key: %s" % kv[0])
                params[kv[0]] = kv[1]
            else:
                raise SystemExit("unknown option: %s" % a)
        else:
            if src is None:
                src = a
            else:
                raise SystemExit("too many command-line arguments")
    return dict(src=src, dest=dest, params=params)


def main():
    import sys

    cmd = _parse_args(sys.argv[1:])
    src, dest, params = map(cmd.get, ['src', 'dest', 'params'])

    if src is None:
        src_text = sys.stdin.read()
    else:
        with open(src, "rb") as f:
            src_text = f.read()
    src_text = src_text.decode('utf-8')

    rendered = render(src_text, params)

    rendered = rendered[1:] if rendered.startswith('\n') else rendered  # just a little bit walkaround (this is a mako's spec?)
    rendered = rendered + '\n' if not rendered.endswith('\n') else rendered  # same as the above

    rendered = rendered.encode('utf-8')
    if dest is None:
        sys.stdout.write(rendered)
    else:
        with open(dest, "wb") as f:
            f.write(rendered)


if __name__ == '__main__':
    main()
