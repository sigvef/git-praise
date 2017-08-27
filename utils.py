def rightpad(string, length):
    string = str(string)
    truncated = string[:length]
    if len(string) >= length + 1:
        truncated = truncated[:-1] + '…'
    return truncated + ' ' * (length - len(truncated))

def leftpad(string, length):
    string = str(string)
    return rightpad(string[::-1], length)[::-1]

def progress_bar(progress, width=20):
    bar_width = width - 17
    completed_blocks = int(progress * bar_width)
    return ('Loading: |' +
            '█' * completed_blocks +
            '-' * (bar_width - completed_blocks) +
            '| %s%%' % (int(progress * 1000) / 10.))
