# -*- coding: UTF-8 -*-
import pynvim
import os
import re


@pynvim.plugin
class Main(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False

    @pynvim.function('GetFileContents', sync=True)
    def getFileContents(self, args):
        # get the current buffer
        buf = self.nvim.current.buffer
        # regex patterns
        pattern = re.compile(r'^\s*\*\s\[(?P<cat>.+?)\]\((?P<dir>.+?)\)')
        # appendedpattern = re.compile(r'\s*\[\s\d+\s\]$')
        # appendedpattern = re.compile(r'\s*\[\s.+\d+\s\]$')
        appendedpattern = re.compile(r'\s*\bfiles:\s\d+\b$')
        # totalappendedpattern = re.compile(r'.*\s\[\s\d+\s\]$')
        totalappendedpattern = re.compile(r'.*\s*\bfiles:\s\d+\b$')
        # get the directory of the current buffer
        cur_dir_path = os.path.dirname(buf.name)
        # get the list of files/directories in the current directory
        directories = os.listdir(cur_dir_path)

        if (self.toggle):
            for i in range(len(buf)):
                # get line index i of buffer
                line = buf[i]
                lengthofline = len(line)
                # check if line is in the format we are concerned with
                m = pattern.match(line)
                # check if line already has appended info
                a = totalappendedpattern.match(line)
                # find any backticks
                backticks = len(re.findall(r'`.*?`', line)) * 2

                # if line is format we are concerned with and has
                # not been appended with info.
                if (m and not a):
                    # get the group in pattern that has the directory
                    match_dir = m.group('dir')
                    # get the path of the directory in link
                    match_dir_path = os.path.dirname(match_dir)

                    # if found directory in line matches a directory in current
                    # buffer directory
                    if (match_dir_path in directories):
                        # get the files/directories of found directory
                        match_dir_path_dirs = os.listdir(match_dir_path)

                        # find how many spaces to append.
                        # get the longest char line.
                        # TODO:
                        visiblelength = lengthofline - \
                            (len(match_dir) + 4) - backticks
                        spaces = ""
                        if (visiblelength < 60):
                            spaces += " " * (60 - visiblelength)

                        # append info
                        # buf[i] += ' ' + \
                        # '[ ' + str(len(match_dir_path_dirs)) + ' ]'

                        buf[i] += spaces + "files: " + \
                            str(len(match_dir_path_dirs))

        # if not toggled on, remove appended info if any
        else:
            for i in range(len(buf)):
                line = buf[i]
                # get the substring without appended info
                buf[i] = re.sub(appendedpattern, '', line)

    @ pynvim.command('MemMachineToggle', nargs=0, range=None)
    def testcommand(self):
        self.toggle = not self.toggle
        self.nvim.command('call GetFileContents()')

    @ pynvim.autocmd('BufWinEnter', pattern='*.md', eval=None, sync=False)
    def on_vimwikienter(self):
        is_enabled = self.nvim.eval('g:MemMachineEnable')
        buf = self.nvim.current.buffer
        MemIndex = self.nvim.eval('g:MemMachineIndex')
        if (buf.name == MemIndex):
            self.nvim.command('setlocal nowrap')
            if (is_enabled):
                self.toggle = True
            else:
                self.toggle = False
            self.nvim.command('call GetFileContents()')
