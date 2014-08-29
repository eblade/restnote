import pprint
from lxml import etree
from ansicolor import strip_escapes
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter
except ImportError:
    _have_pygment = False
else:
    _have_pygment = True

BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NORMAL = "\033[0;0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
DEFAULT = "\033[39m"
WHITE = "\033[37m"
BACK_BLUE = "\033[44m"
BACK_DEFAULT = "\033[49m"

pp = pprint.PrettyPrinter(indent=2)


class TerminalLogger:
    def __init__(self):
        self.mute = False
        self.smute = []
        self.graphical = False
        if _have_pygment:
            self.formatter = TerminalFormatter()
            self.lexer = get_lexer_by_name('xml')

    def log(self, desc, data=None, data_type=None):
        if self.mute or data_type in self.smute:
            return
        if data_type == 'comment':
            print(BLUE + desc.strip() + NORMAL)
            return
        if data_type == 'title':
            print(BOLD + BLUE + desc.strip() + NORMAL)
            return
        if data_type == 'table':
            lengths = [len(strip_escapes(x)) for x in desc]
            for row in data:
                lengths = [max(lengths[n], len(strip_escapes(x)))
                           for n, x in enumerate(row)]
            fs = '  '.join([('%%-%is' % l) for l in lengths])
            print(fs % tuple(desc))
            for row in data:
                print(fs % tuple(row))
            return
        if data_type == 'error':
            print(BOLD + RED + desc + NORMAL)
        elif data_type == 'ok':
            print(BOLD + GREEN + desc + NORMAL)
        elif desc is not None:
            print("%s%s%s" % (BOLD, desc, NORMAL))
        if data is not None:
            if _have_pygment and data_type == 'xml':
                try:
                    data = etree.tostring(data)
                except AttributeError:
                    pass
                except TypeError:
                    pass
                try:
                    data = data.decode()
                except AttributeError:
                    data = str(data)
                print(highlight(data, self.lexer, self.formatter))
            elif data_type in ('pp', 'error'):
                pp.pprint(data)
            else:
                print(data)

    def colorify(self, value, color=None):
        if color is None:
            return value
        elif color == 'gray':
            return DIM + value + NORMAL
        elif color == 'green':
            return GREEN + BOLD + value + NORMAL
        elif color == 'blue':
            return BLUE + value + NORMAL
        elif color == 'red':
            return RED + value + NORMAL
        elif color == 'yellow':
            return YELLOW + value + NORMAL
        elif color == 'gray':
            return DIM + value + NORMAL
        elif color == 'gray':
            return DIM + value + NORMAL
        elif color == 'black':
            return BOLD + value + NORMAL
        else:
            print("Uknown color '%s'" % color)
            return value

    def close(self):
        pass
