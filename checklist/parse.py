import os.path

from . import model


class ChecklistParser(object):
    """
    Parse an input text file to generate a text file. Try to be tolerant of
    weird ways of formatting things, like Markdown bulleted lists, plain text,
    etc.
    """
    def __init__(self, filename):
        self.name = os.path.splitext(os.path.basename(filename))[0]
        self.f = open(filename)

    def parse(self):
        # XXX super naive approach, just one item per line
        category = model.Category(name=None)
        for line in self.f:
            line = line.strip()
            if line.startswith('* '):
                line = line[2:]
            category.items.append(line)
        checklist = model.Checklist(name=self.name, categories=[category])
        return checklist
