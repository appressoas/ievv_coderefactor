import re

PATTERN = re.compile(r'^\s*//.*?$')


def strip_json_comments(jsonstring):
    lines = []
    for line in jsonstring.splitlines():
        if PATTERN.match(line):
            continue
        lines.append(line)
    return '\n'.join(lines)
