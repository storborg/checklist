import sys
import argparse

from . import __version__


def register(opts):
    pass


def verify(opts):
    print("Checklist doesn't work yet, it can't verify anything.")
    return 1


def check(opts):
    pass


def view(opts):
    pass


def main(argv=sys.argv):
    p = argparse.ArgumentParser(
        description='A tool to manage checklists.')

    p.add_argument('--version', action='store_true',
                   help='Print program version.')
    p.add_argument('-v', '--verbose', action='store_true',
                   help='Print verbose debugging information.')

    subparsers = p.add_subparsers(help='sub-command help')

    p_register = subparsers.add_parser(
        'register',
        help='Register a new checklist, or update an existing one.')
    p_register.add_argument('filename')
    p_register.set_defaults(function=register)

    p_verify = subparsers.add_parser(
        'verify',
        help='Verify that the local checklist has been completed.')
    p_verify.add_argument('-p', '--path')
    p_verify.set_defaults(function=verify)

    p_check = subparsers.add_parser(
        'check',
        help='Go through the checklist.')
    p_check.add_argument('-p', '--path')
    p_check.set_defaults(function=check)

    p_view = subparsers.add_parser(
        'view',
        help='View available checklists.')
    p_view.add_argument('name')
    p_view.set_defaults(function=view)

    opts = p.parse_args(argv[1:])
    if opts.version:
        print(__version__)
    elif hasattr(opts, 'function'):
        return opts.function(opts)
    else:
        p.print_help()
