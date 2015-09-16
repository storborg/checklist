import sys
import argparse

from datetime import datetime

import six

from . import __version__, model
from .parse import ChecklistParser


def register_command(opts):
    registry = model.Registry.load()
    checklist = ChecklistParser(opts.filename).parse()
    registry[checklist.name] = checklist
    registry.save()
    print("Registered checklist as '%s'." % checklist.name)


def verify_command(opts):
    registry = model.Registry.load()
    project = model.Project.load(registry)
    return 0 if project.verify() else 1


def pick_checklist(registry):
    checklist_names = sorted(registry.keys())
    while True:
        for ii, checklist_name in enumerate(checklist_names):
            print("[%d] %s" % (ii, checklist_name))
        index = six.input('>>> ')
        try:
            return checklist_names[int(index)]
        except (IndexError, TypeError, ValueError):
            print("")
            print("Please select a number from the list:")


def new_project(registry):
    print("No checklist is registered for this project tree. "
          "Please select one:")
    checklist_name = pick_checklist(registry)
    return model.Project(registry, checklist_name)


def input_yesno(prompt='[Y/n] '):
    while True:
        resp = six.input('[Y/n] ').strip().lower()
        if (resp == '') or resp.startswith('y'):
            return True
        elif resp.startswith('n'):
            return False


def check_item(mtime, item, last_check, category):
    print('-' * 40)
    if category.name:
        print("%s [%s]" % (item, category.name))
    else:
        print(item)
    if not last_check:
        print("-- Never checked.")
    else:
        datestr = datetime.fromtimestamp(last_check.timestamp).\
            strftime("%Y-%m-%d")
        print("-- Last checked on %s by %s." % (datestr, last_check.username))
    return input_yesno()


def check_command(opts):
    registry = model.Registry.load()
    project = model.Project.load(registry)
    if not project:
        project = new_project(registry)
    print("Using %s checklist. Let's go." % project.checklist.name)
    modtime = project.check_tree_time()
    for item, last_check, category in project.items_to_check():
        if check_item(modtime, item, last_check, category):
            project.mark_checked(item, category)
    project.save()
    print("Checklist is complete!")


def view_command(opts):
    registry = model.Registry.load()
    checklist = registry[opts.name]
    for category in checklist.categories.values():
        if category.name:
            print("%s:\n" % category.name)
        for item in category.items:
            print("* %s" % item)


def list_command(opts):
    registry = model.Registry.load()
    print("Checklists available:")
    for checklist_name in registry:
        print("- %s" % checklist_name)


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
    p_register.set_defaults(function=register_command)

    p_verify = subparsers.add_parser(
        'verify',
        help='Verify that the local checklist has been completed.')
    # p_verify.add_argument('-p', '--path')
    p_verify.set_defaults(function=verify_command)

    p_check = subparsers.add_parser(
        'check',
        help='Go through the checklist.')
    # p_check.add_argument('-p', '--path')
    p_check.set_defaults(function=check_command)
    # XXX add a feature here to check everything even if the check is already
    # current
    # XXX add a feature to check only a specific category

    p_view = subparsers.add_parser(
        'view',
        help='View a checklist.')
    p_view.add_argument('name')
    p_view.set_defaults(function=view_command)

    p_list = subparsers.add_parser(
        'list',
        help='View available checklists.')
    p_list.set_defaults(function=list_command)

    opts = p.parse_args(argv[1:])
    if opts.version:
        print(__version__)
    elif hasattr(opts, 'function'):
        return opts.function(opts)
    else:
        p.print_help()
