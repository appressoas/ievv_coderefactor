import re


class AbstractRenamer(object):
    def replace(self, string):
        raise NotImplementedError()


class StringRenamer(AbstractRenamer):
    def __init__(self, from_string, to_string):
        self.from_string = from_string
        self.to_string = to_string

    def replace(self, string):
        return string.replace(self.from_string, self.to_string)


class RegexRenamer(AbstractRenamer):
    def __init__(self, pattern, replacement):
        self.pattern = re.compile(pattern, re.MULTILINE)
        self.replacement = replacement

    def replace(self, string):
        new_string = self.pattern.sub(self.replacement, string)
        return new_string


RENAMER_REGISTRY = {
    'StringRenamer': StringRenamer,
    'RegexRenamer': RegexRenamer
}
