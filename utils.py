def rightpad(string, length):
    string = str(string)
    truncated = string[:length]
    if len(string) > length + 1:
        truncated = truncated[:length - 1] + '…'
    return truncated + ' ' * (length - len(truncated))

def leftpad(string, length):
    string = str(string)
    return rightpad(string[::-1], length)[::-1]
