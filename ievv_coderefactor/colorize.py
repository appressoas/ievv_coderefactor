try:
    from termcolor import colored
except ImportError:
    DISABLE_COLORS = True
else:
    DISABLE_COLORS = False

#: Red color constant for :func:`.ievv_colorize`.
COLOR_RED = 'red'

#: Blue color constant for :func:`.ievv_colorize`.
COLOR_BLUE = 'blue'

#: Yellow color constant for :func:`.ievv_colorize`.
COLOR_YELLOW = 'yellow'

#: Grey color constant for :func:`.ievv_colorize`.
COLOR_GREY = 'grey'

#: Green color constant for :func:`.ievv_colorize`.
COLOR_GREEN = 'green'


def colored_text(text, color, bold=False):
    """
    Colorize a string for stdout/stderr.

    Examples:

        Print blue text::

            print(colorize.colored_text('Test', color=colorize.COLOR_BLUE))

        Print bold red text::

            print(colorize.colored_text('Test', color=colorize.COLOR_RED, bold=True))

    Args:
        text: The text (string) to colorize.
        color: The color to use.
            Should be one of:

            - :obj:`.COLOR_RED`
            - :obj:`.COLOR_BLUE`
            - :obj:`.COLOR_YELLOW`
            - :obj:`.COLOR_GREY`
            - :obj:`.COLOR_GREEN`
            - ``None`` (no color)
        bold: Set this to ``True`` to use bold font.
    """
    if DISABLE_COLORS:
        return text
    attrs = []
    if bold:
        attrs.append('bold')
    return colored(text, color=color, attrs=attrs)
