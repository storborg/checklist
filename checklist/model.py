import os
import os.path


default = object()


def get_default_registry_path():
    return os.path.join(os.path.expanduser('~'), '.checklists')


class Checklist(object):

    def __init__(self, name):
        pass


class ChecklistRegistry(dict):

    @classmethod
    def load(self, registry_path=default):
        pass

    def save(self, registry_path=default):
        pass
