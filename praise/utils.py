# -*- coding: utf-8 -*-
def rightpad(string, length):
    string = str(string)
    truncated = string[:length]
    if len(string) >= length + 1:
        truncated = truncated[:-1] + u'…'
    return truncated + u' ' * (length - len(truncated))


def leftpad(string, length):
    string = str(string)
    return rightpad(string[::-1], length)[::-1]


def progress_bar(progress, width=20):
    bar_width = width - 17
    completed_blocks = int(progress * bar_width)
    return (u'Loading: |' +
            u'█' * completed_blocks +
            u'-' * (bar_width - completed_blocks) +
            u'| %s%%' % (int(progress * 1000) / 10.))


def is_binary_string(string):
    textchars = (bytearray({7, 8, 9, 10, 12, 13, 27} |
                 set(range(0x20, 0x100)) - {0x7f}))
    return bool(string.translate(None, textchars))
