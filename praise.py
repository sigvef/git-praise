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
        sidebar_width)
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
    blame_entries = sorted(
        repo.blame_incremental('HEAD', filename),
        key=lambda entry: entry.orig_linenos[0])

    # make display entires
    display_entries = []
    for entry in blame_entries:
        line_numbers = entry.orig_linenos[0]
        start = entry.orig_linenos[0] - 1
        end = entry.orig_linenos[-1]
        lines = highlighted[start:end]
        display_entries.append(
            DisplayEntry(commit=entry.commit,
            lines=lines,
            line_number_start=start + 1))

    # measure display entires
    name_length = max([len(display_entry.name)
                       for display_entry in display_entries])
    author_name_length = max([
        len(display_entry.author_name)
        for display_entry in display_entries])

    line_number_width = int(math.log(len(highlighted), 10) + 0.5)

    sidebar_width = sum((
        name_length,
        author_name_length,
        19,
        line_number_width))

    print(header(filename, repo, sidebar_width))
    terminal_height, terminal_width = os.popen(
        'stty size', 'r').read().split()
    for display_entry in display_entries:
        line = display_entry.render(
            author_name_length=author_name_length,
            name_length=name_length,
            total_line_count=len(highlighted),
            width=int(terminal_width))
        print(line)
