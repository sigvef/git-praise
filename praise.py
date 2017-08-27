from collections import namedtuple
from display_entry import DisplayEntry
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_for_filename
from termcolor import colored
from utils import leftpad
from utils import progress_bar
from utils import rightpad
import hashlib
import math
import os
import pygments

formatter = get_formatter_by_name('console')
Entry = namedtuple('Entry', ['commit', 'line_numbers'])

def entry_from_blame_entry(blame_entry):
    return Entry(commit=blame_entry.commit,
                 line_numbers=[blame_entry.linenos[0],
                               blame_entry.linenos[-1]])

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
    entries = list(sorted(
        map(entry_from_blame_entry, repo.blame_incremental('HEAD', filename)),
        key=lambda entry: entry.line_numbers))

    merged_entries = [entries[0]]
    for entry in entries[1:]:
        previous_entry = merged_entries[-1]
        if previous_entry.commit == entry.commit:
            previous_entry.line_numbers[1] = entry.line_numbers[1]
        else:
            merged_entries.append(entry)

    terminal_height, terminal_width = os.popen(
        'stty size', 'r').read().split()

    # make display entries
    display_entries = []
    for i, entry in enumerate(merged_entries):
        print('\r' + progress_bar(i / len(merged_entries), width=int(terminal_width)), end='')
        line_numbers = entry.line_numbers[0]
        start = entry.line_numbers[0] - 1
        end = entry.line_numbers[1]
        lines = highlighted[start:end]
        display_entries.append(
            DisplayEntry(commit=entry.commit,
            lines=lines,
            line_number_start=start + 1))
    print('\r' + ' ' * int(terminal_width) + '\r', end='')

    # measure display entries
    name_length = max([len(display_entry.name)
                       for display_entry in display_entries])
    author_name_length = max([
        len(display_entry.author_name)
        for display_entry in display_entries])

    line_number_length = int(math.log(len(highlighted), 10) + 1)

    if int(terminal_width) < 80:
        author_name_length = 0

    sidebar_width = sum((
        2,
        name_length,
        1 if author_name_length else 0,
        author_name_length,
        1,
        20,
        1,
        line_number_length))

    colors = ('red',
              'blue',
              'yellow',
              'magenta',
              'cyan',
              'white',)
    commit_colors = {}
    for display_entry in display_entries:
        if display_entry.name not in commit_colors:
            commit_colors[display_entry.name] = colors[
                int(hashlib.sha1(display_entry.name.encode('utf-8')).hexdigest(), 16) % len(colors)]

    print(header(filename, repo, sidebar_width))
    for i, display_entry in enumerate(display_entries):
        line = display_entry.render(
            author_name_length=author_name_length,
            name_length=name_length,
            line_number_length=line_number_length,
            sidebar_width=sidebar_width,
            commit_color=commit_colors[display_entry.name],
            width=int(terminal_width))
        print(line)
