# -*- coding: UTF-8 -*-
import pynvim
import os
import re


@pynvim.plugin
class Main(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False
        # self.nvim.command("sy match memMachineGood '\vgood$'")

    @pynvim.function('GetFileContents', sync=True, allow_nested=False)
    def getFileContents(self, args):
        # get the current buffer
        buf = self.nvim.current.buffer
        # pattern to see if file already has appended info
        appendedpattern = re.compile(r'.*\s*\bfiles:\s\d+\b$')
        onlyappendedpattern = re.compile(r'\s*\bfiles:\s\d+\b$')
        # regex patterns
        unappendedpattern = re.compile(
            r'^\s*\*\s\[(?P<cat>.+?)\]\((?P<dir>.+?)\)')

        # get the directory of the current buffer
        cur_dir_path = os.path.dirname(buf.name)
        # get the list of files/directories in the current directory
        directories = os.listdir(cur_dir_path)

        # check if already appended
        for i in range(len(buf)):
            line = buf[i]
            appendedmatch = appendedpattern.match(line)
            unappendedmatch = unappendedpattern.match(line)

            # get nvim highlight source
            src_id = self.nvim.new_highlight_source()

            if (self.toggle):
                if (appendedmatch):
                    lengthofunappended = len(
                        re.sub(onlyappendedpattern, '', line))
                    # highlight line
                    buf.add_highlight(
                        "Comment", i, lengthofunappended, -1, src_id)
                elif (unappendedmatch and not appendedmatch):
                    backticks = len(re.findall(r'`.*?`', line)) * 2
                    match_dir = unappendedmatch.group('dir')
                    match_dir_path = os.path.dirname(match_dir)
                    if (match_dir_path in directories):
                        match_dir_path_dirs = os.listdir(match_dir_path)
                        lengthofline = len(line)
                        visiblelength = lengthofline - \
                            (len(match_dir) + 4) - backticks
                        spaces = ""
                        if (visiblelength < 60):
                            spaces += " " * (60 - visiblelength)
                        # add file info
                        buf[i] += spaces + "files: " + \
                            str(len(match_dir_path_dirs)-1)
                        # highlight line
                        buf.update_highlights(
                            src_id, [("Comment", i, lengthofline, -1)], clear=True, async_=False)

            else:
                if (appendedmatch):
                    buf[i] = re.sub(onlyappendedpattern, '', line)

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
            if (buf.valid == True):
                self.nvim.command('call GetFileContents()')
