import os
import os.path
import getpass
import json
import time


default = object()

format_version = 1


def get_default_registry_path():
    return os.path.join(os.path.expanduser('~'), '.checklists')


def get_default_project_path():
    return os.path.join(os.getcwd(), '.checklist')


def json_dump_pretty(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '))


class Category(object):

    def __init__(self, name, items=None):
        self.name = name
        self.items = items or []

    def serialize(self):
        return {
            'name': self.name,
            'items': self.items,
        }

    @classmethod
    def deserialize(cls, data):
        return cls(
            name=data['name'],
            items=data['items'],
        )


class Checklist(object):

    def __init__(self, name, categories=None):
        self.name = name
        categories = categories or []
        self.categories = {cat.name: cat for cat in categories}

    def serialize(self):
        return {
            'name': self.name,
            'categories': [cat.serialize() for cat in
                           self.categories.values()],
        }

    @classmethod
    def deserialize(cls, data):
        return cls(
            name=data['name'],
            categories=[Category.deserialize(cat_data)
                        for cat_data in data['categories']],
        )


class FormatError(Exception):
    pass


class Registry(dict):

    @classmethod
    def load(cls, registry_path=default):
        if registry_path == default:
            registry_path = get_default_registry_path()
        if os.path.exists(registry_path):
            with open(registry_path) as f:
                data = json.load(f)
                version = data.pop('version')
                if version == 1:
                    return cls({
                        name: Checklist.deserialize(checklist)
                        for name, checklist
                        in data.items()
                    })
                else:
                    raise FormatError(
                        "The version of checklist used to save this registry "
                        "is newer than your current version: please upgrade "
                        "with 'pip install checklist'.")
        else:
            return cls()

    def save(self, registry_path=default):
        if registry_path == default:
            registry_path = get_default_registry_path()
        # Serialize to a string first, then save to the file, to avoid saving
        # if there's an error.
        data = {name: checklist.serialize()
                for name, checklist in self.items()}
        data['version'] = format_version
        s = json_dump_pretty(data)
        with open(registry_path, 'w') as f:
            f.write(s)


class Check(object):

    def __init__(self, description, category, username=None, timestamp=None):
        self.description = description
        self.category = category
        self.username = username or getpass.getuser()
        self.timestamp = timestamp or time.time()

    def serialize(self):
        return {
            'description': self.description,
            'category': self.category,
            'username': self.username,
            'timestamp': self.timestamp,
        }

    @classmethod
    def deserialize(cls, data):
        return cls(
            description=data['description'],
            category=data['category'],
            username=data['username'],
            timestamp=data['timestamp'],
        )


class Project(object):

    def __init__(self, registry, checklist_name, history=None):
        self.checklist_name = checklist_name
        self.checklist = registry[self.checklist_name]
        self.history = history or []
        self.last_checks = {}
        # XXX this is gonna be a slow approach for a large project: ideally,
        # traverse from the most recent and then stop when all current items
        # have been checked.
        for check in self.history:
            self.last_checks[(check.description, check.category)] = check

    def mark_checked(self, item, category):
        self.history.append(Check(
            description=item,
            category=category.name,
        ))

    @classmethod
    def load(cls, registry, path=default):
        if path == default:
            path = get_default_project_path()
        if not os.path.exists(path):
            return
        with open(path) as f:
            data = json.load(f)
            version = data.pop('version')
            if version == 1:
                return cls(registry,
                           checklist_name=data['checklist_name'],
                           history=[Check.deserialize(check_data) for
                                    check_data in data['history']])
            else:
                raise FormatError(
                    "The version of checklist used to save this registry "
                    "is newer than your current version: please upgrade "
                    "with 'pip install checklist'.")

    def save(self, path=default):
        if path == default:
            path = get_default_project_path()
        data = {
            'version': format_version,
            'checklist_name': self.checklist_name,
            'history': [check.serialize() for check in self.history],
        }
        s = json_dump_pretty(data)
        with open(path, 'w') as f:
            f.write(s)

    def check_tree_time(self):
        # XXX Get this from the Project instead?
        path = os.getcwd()
        # XXX
        project_file_path = os.path.join(path, '.checklist')
        return max(os.path.getmtime(fp) for fp in
                   (filepaths for filepaths, dirs, files in os.walk(path))
                   if fp != project_file_path)

    def verify(self):
        modtime = self.check_tree_time()
        for category in self.checklist.categories.values():
            for item in category.items:
                check = self.last_checks.get((item, category.name))
                if (not check) or (check.timestamp < modtime):
                    return False
        return True

    def items_to_check(self, category=None):
        if category:
            category = {cat.name: cat for cat in
                        self.checklist.categories}[category]
            categories = [category]
        else:
            categories = self.checklist.categories

        modtime = self.check_tree_time()
        for category in categories.values():
            for item in category.items:
                last_check = self.last_checks.get((item, category.name))
                if (not last_check) or (last_check.timestamp < modtime):
                    yield item, last_check, category
