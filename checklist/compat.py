import sys


PY3 = sys.version_info[0] > 2


if not PY3:
    input = raw_input
else:
    input = input
