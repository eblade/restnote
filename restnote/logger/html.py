import pprint
from lxml import etree
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
except ImportError:
    _have_pygment = False
else:
    _have_pygment = True

pp = pprint.PrettyPrinter(indent=2)


class HtmlLogger:
    def __init__(self):
        self.mute = False
        self.smute = []
        self.graphical = True
        if _have_pygment:
            self.formatter = HtmlFormatter()
            self.lexer = get_lexer_by_name('xml')
        print("<html><head><style>\n")
        print(self.formatter.get_style_defs())
        print(".header { font-family: arial; font-weight: bold }")
        print(""".code { background-color: #fafafa; border-left: 2px solid #aaa;
                  padding: 5px; margin-top: 5px; margin-bottom: 5px } """)
        print(""".comment { font-family: arial; font-weight:
                  normal; color: blue; margin-bottom: 20px;
                  font-style: italic; margin-top: 20px}""")
        print(""".title { font-family: arial; font-size: 24; font-weight:
                  bold; color: blue; margin-bottom: 20px;
                  margin-top: 20px}""")
        print(""".error { font-family: arial; font-size: 12; font-weight:
                  bold; color: red; margin-bottom: 20px;
                  margin-top: 20px}""")
        print(""".error { font-family: arial; font-size: 12; font-weight:
                  bold; color: green; margin-bottom: 20px;
                  margin-top: 20px}""")
        print(""" table { font-family: arial; font-size: 12; font-weight:
                  normal; margin-bottom: 20px;
                  margin-top: 20px}""")
        print(""" th { font-family: arial; font-size: 12; font-weight:
                  bold; text-align: left }""")
        print(""" td { border-top: 1px solid #ccc }""")
        print("</style></head><body>")
        self.counter = 0

    def get_id(self):
        self.counter += 1
        return "obj%i" % self.counter

    def log(self, desc, data=None, data_type=None):
        if self.mute or data_type in self.smute:
            return
        if data_type == 'comment':
            print("<div class=\"comment\">%s</div>" % desc)
            return
        if data_type == 'title':
            print("<div class=\"title\">%s</div>" % desc)
            return
        if data_type == 'table':
            print("<table><tr>")
            for heading in desc:
                print('<th>%s</th>' % heading)
            print("</tr>")
            for row in data:
                print("<tr>")
                for col in row:
                    print('<td>%s</td>' % col)
                print("</tr>")
            print("</table>")
            return
        if data_type == 'error':
            print("<div class=\"error\">%s</div>" % desc)
        elif data_type == 'ok':
            print("<div class=\"ok\">%s</div>" % desc)
        elif desc is not None:
            print("<div class=\"header\">%s</div>" % desc)
        if data is not None:
            print("<div class=\"code\">")
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
                print(highlight(str(data), self.lexer, self.formatter))
            elif data_type == 'pp':
                print("<pre>")
                pp.pprint(data)
                print("</pre>")
            else:
                data = (str(data).replace('&', '&amp;').replace('<', '&lt;')
                        .replace('>', '&gt'))
                print("<pre>%s</pre>" % data)
            print("</div>")

    def close(self):
        print("</body></html>\n")
