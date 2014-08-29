import pprint
from lxml import etree
import logging

pp = pprint.PrettyPrinter(indent=2)


class FileLogger:
    def __init__(self, filename, level=logging.DEBUG):
        self.mute = False
        self.smute = []
        self.graphical = False
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(filename, 'w')
        self.fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)

    def log(self, desc, data=None, data_type=None):
        if self.mute or data_type in self.smute:
            return
        if data_type in ('comment', 'title'):
            self.logger.info(desc.strip())
            return
        if data_type == 'table':
            lengths = [len(x) for x in desc]
            output = ""
            for row in data:
                lengths = [max(lengths[n])
                           for n, x in enumerate(row)]
            fs = '  '.join([('%%-%is' % l) for l in lengths])
            output += fs % tuple(desc) + '\n'
            for row in data:
                output += fs % tuple(row) + '\n'
            self.logger.info(output)
            return
        if data_type == 'error':
            self.logger.error(desc.strip())
        if data_type == 'warning':
            self.logger.warn(desc.strip())
        if data_type == 'debug':
            self.logger.debug(desc.strip())
        if data_type in ('info', 'ok') or data_type is None:
            self.logger.info(desc.strip())
        if data is not None:
            if data_type == 'xml':
                try:
                    data = etree.tostring(data)
                except AttributeError:
                    pass
                except TypeError:
                    pass
                data = str(data)
                self.logger.info(data)
            elif data_type == 'pp':
                self.logger.info(pp.pformat(data))
            else:
                self.logger.info(data)

    def close(self):
        try:
            self.fh.close()
        except:
            pass
