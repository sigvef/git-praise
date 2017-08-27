from display_entry import DisplayEntry
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_for_filename
from termcolor import colored
from utils import leftpad
from utils import rightpad
import math
import os
import pygments


def praise(filename, repo):
    formatter = get_formatter_by_name('console')
    terminal_height, terminal_width = os.popen(
        'stty size', 'r').read().split()
    with open(filename) as f:
        text = f.read()
    lexer = get_lexer_for_filename(filename)
    highlighted = pygments.highlight(
        text, lexer, formatter).split('\n')
    blame_entries = repo.blame_incremental('HEAD', filename)
    sorted_blame_entries = sorted(
        blame_entries, key=lambda entry: entry.orig_linenos[0])
    display_entries = []
    for entry in sorted_blame_entries:
        line_numbers = entry.orig_linenos
        start = entry.orig_linenos[0] - 1
        end = entry.orig_linenos[-1]
        lines = highlighted[start:end]
        display_entries.append(
            DisplayEntry(commit=entry.commit,
            lines=lines,
            line_number_start=start + 1))
    number_of_display_entries = len(display_entries)
    name_length = max([len(display_entry.name)
                       for display_entry in display_entries])
    author_name_length = max([
        len(display_entry.author_name)
        for display_entry in display_entries])
    relative_path = repo.tree()[filename].path
    basename = os.path.basename(relative_path)
    formatted_relative_path = leftpad(
        '(repo)/' + relative_path[:-len(basename)],
        20)
    header = ''.join([
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

    print(header)
    for display_entry in display_entries:
        line = display_entry.render(
            author_name_length=author_name_length,
            name_length=name_length,
            total_line_count=number_of_display_entries,
            width=int(terminal_width))
        print(line)
