from termcolor import colored
from utils import leftpad
from utils import rightpad
import math


class DisplayEntry(object):
    def __init__(
            self,
            commit=None,
            lines=None,
            line_number_start=0):
        self.commit = commit
        self.lines = lines
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
            total_line_count=0,
            same_commit=False,
            width=80):
        output = []
        author_name = rightpad(self.author_name, author_name_length)
        name = rightpad(self.name, name_length)
        if width < 80:
            author_name = ''
        commit_message = ' '.join(
            filter(lambda x: x,
                map(lambda x: x.strip(),
                   self.commit.message.split('\n'))))
        commit_message_munched_length = 0
        for i, line in enumerate(self.lines):
            line = line[:width]
            formatted_line_number = leftpad(
                self.line_number_start + i,
                int(math.log(total_line_count, 10) + 1)) + '.'

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


            attrs = ['dark']
            if i == len(self.lines) - 1:
                attrs.append('underline')

            if i != 0:
                name = ' ' * len(name)
                author_name = ' ' * len(author_name)
        
            output.append(''.join([
                colored(name,
                        'yellow',
                        'on_grey',
                        attrs=attrs),
                colored(' ',
                        'yellow',
                        'on_grey',
                        attrs=attrs),
                colored(author_name,
                        'green',
                        'on_grey',
                        attrs=attrs),
                colored(' ' if author_name else '',
                        'green',
                        'on_grey',
                        attrs=attrs),
                colored(commit_message_part,
                        'magenta',
                        'on_grey',
                        attrs=attrs),
                colored(' ',
                        'grey',
                        'on_grey',
                        attrs=attrs),
                colored(formatted_line_number.strip(),
                        'grey',
                        'on_grey',
                        attrs=attrs),
                colored(' ', 'grey'),
                colored(line, 'white'),
            ]))
        return '\n'.join(output)