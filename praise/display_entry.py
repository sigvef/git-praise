# -*- coding: utf-8 -*-
from termcolor import colored
from praise.utils import leftpad
from praise.utils import rightpad
import re

ANSI_REGEX = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')


def escape_ansi(line):
    return ANSI_REGEX.sub('', line)


class DisplayEntry(object):
    def __init__(
            self,
            commit=None,
            lines_range=None,
            line_number_start=0):
        self.commit = commit
        self.lines_range = lines_range
        self.line_number_start = line_number_start

        self.name = self.commit.name_rev.split(' ')[1]
        if self.name.startswith('remotes/'):
            self.name = self.commit.hexsha[:7]
        if len(self.name) > 20:
            self.name = rightpad(self.name, 20)
        self.author_name = self.commit.author.name.split(' ')[0]

    def render(
            self,
            author_name_length=0,
            name_length=0,
            line_number_length=0,
            sidebar_width=0,
            commit_color='on_grey',
            width=80):
        output = []
        author_name = rightpad(self.author_name, author_name_length)
        name = rightpad(self.name, name_length)
        if author_name_length == 0:
            author_name = ''
        commit_message = u' '.join(
            filter(lambda x: x,
                   map(lambda x: x.strip(),
                       self.commit.message.split(u'\n'))))
        for i, line in enumerate(self.lines):
            formatted_line_number = leftpad(
                self.line_number_start + i,
                line_number_length) + '.'

            commit_message_part_length = (
                20 +
                len(formatted_line_number) -
                len(formatted_line_number.strip()))
            commit_message_part = commit_message[
                :commit_message_part_length]
            commit_message_part = commit_message_part.strip()
            commit_message_part = rightpad(
                commit_message_part, commit_message_part_length)
            if i == len(self.lines) - 1:
                commit_message_part = rightpad(
                    commit_message,
                    commit_message_part_length)
            commit_message = commit_message[len(commit_message_part):]

            attrs = []
            if i == len(self.lines) - 1:
                attrs.append('underline')

            if i != 0:
                name = ' ' * len(name)
                author_name = ' ' * len(author_name)

            output.append(u''.join([
                colored(u'█ ', commit_color, 'on_grey', attrs=attrs),
                colored(name, commit_color, 'on_grey', attrs=attrs),
                colored(u' ', commit_color, 'on_grey', attrs=attrs),
                colored(author_name, 'green', 'on_grey', attrs=attrs),
                colored(u' ' if author_name else '',
                        'green', 'on_grey', attrs=attrs),
                colored(commit_message_part,
                        commit_color, 'on_grey', attrs=attrs),
                colored(u' ', 'grey', 'on_grey', attrs=['dark'] + attrs),
                colored(formatted_line_number.strip(),
                        u'grey', 'on_grey', attrs=['dark'] + attrs),
                colored(u'┃', 'grey'),
                line,
            ]))
        return u'\n'.join(output)
