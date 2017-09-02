# -*- coding: utf-8 -*-
from pygments.formatters import TerminalTrueColorFormatter


class TruncatingTrueColorFormatter(TerminalTrueColorFormatter):

    def __init__(self, max_width=80, *args, **kwargs):
        TerminalTrueColorFormatter.__init__(self, *args, **kwargs)
        self.max_width = max_width

    # yanxed from TerminalTrueColorFormatter
    def format_unencoded(self, tokensource, outfile):
        unformatted_line_length = 0
        unformatted_truncated_line_length = 0
        for ttype, value in tokensource:
            not_found = True
            while ttype and not_found:
                try:
                    # outfile.write( "<" + str(ttype) + ">" )
                    on, off = self.style_string[str(ttype)]

                    # Like TerminalFormatter, add "reset colors" escape
                    # sequence on newline.
                    spl = value.split('\n')
                    for line in spl[:-1]:
                        if line:
                            unformatted_line_length += len(line)
                            line = line[
                                :self.max_width-unformatted_line_length]
                            unformatted_truncated_line_length += len(line)
                            if ((unformatted_line_length !=
                                 unformatted_truncated_line_length) and
                                    line):
                                line = line[:-1] + u'…'
                            if line:
                                outfile.write(on + line + off)
                        unformatted_line_length = 0
                        unformatted_truncated_line_length = 0
                        outfile.write('\n')
                    if spl[-1]:
                        unformatted_line_length += len(spl[-1])
                        item = spl[-1][:self.max_width-unformatted_line_length]
                        unformatted_truncated_line_length += len(item)
                        if ((unformatted_line_length !=
                             unformatted_truncated_line_length) and item):
                            item = item[:-1] + u'…'
                        if item:
                            outfile.write(on + item + off)

                    not_found = False
                    # outfile.write( '#' + str(ttype) + '#' )

                except KeyError:
                    ttype = ttype[:-1]

            if not_found:
                unformatted_line_length += len(value)
                item = value[:self.max_width-unformatted_line_length]
                unformatted_truncated_line_length += len(value)
                if ((unformatted_line_length !=
                     unformatted_truncated_line_length) and item):
                    item = item[:-1] + u'…'
                if item:
                    outfile.write(item)
