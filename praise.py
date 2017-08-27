from display_entry import DisplayEntry
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_for_filename
from termcolor import colored
from utils import leftpad
from utils import rightpad
import math
import os
import pygments

formatter = get_formatter_by_name('console')

def highlight(filename, text):
    lexer = get_lexer_for_filename(filename)
    return pygments.highlight(text, lexer, formatter).split('\n')

def header(filename, repo, sidebar_width):
    relative_path = repo.tree()[filename].path
    basename = os.path.basename(relative_path)
    formatted_relative_path = leftpad(
        '(repo)/' + relative_path[:-len(basename)],
        sidebar_width + 1)
    return ''.join([
        colored(formatted_relative_path,
                'grey',
                attrs=['dark', 'underline']),
        colored(' ',
                'grey',
                attrs=['underline']),
        colored(basename,
                'white',
                attrs=['bold', 'underline']),
    ])

def praise(filename, repo):
    with open(filename) as f:
        text = f.read()
    highlighted = highlight(filename, text)
    blame_entries = list(sorted(
        repo.blame('HEAD', filename),
        key=lambda entry: entry.linenos[0]))

    # make display entries
    display_entries = []
    for entry in blame_entries:
        print(entry)
        line_numbers = entry.linenos[0]
        start = entry.linenos[0] - 1
        end = entry.linenos[-1]
        lines = highlighted[start:end]
        display_entries.append(
            DisplayEntry(commit=entry.commit,
            lines=lines,
            line_number_start=start + 1))

    # measure display entries
    name_length = max([len(display_entry.name)
                       for display_entry in display_entries])
    author_name_length = max([
        len(display_entry.author_name)
        for display_entry in display_entries])

    line_number_length = int(math.log(len(highlighted), 10) + 1)

    terminal_height, terminal_width = os.popen(
        'stty size', 'r').read().split()

    if int(terminal_width) < 80:
        author_name_length = 0

    sidebar_width = sum((
        name_length,
        1 if author_name_length else 0,
        author_name_length,
        1,
        20,
        1,
        line_number_length))

    print(header(filename, repo, sidebar_width))
    for display_entry in display_entries:
        line = display_entry.render(
            author_name_length=author_name_length,
            name_length=name_length,
            line_number_length=line_number_length,
            sidebar_width=sidebar_width,
            width=int(terminal_width))
        print(line)
