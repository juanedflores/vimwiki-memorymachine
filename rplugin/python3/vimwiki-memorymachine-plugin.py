# -*- coding: UTF-8 -*-
import pynvim
import os
import re


@pynvim.plugin
class Main(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False
        self.lines = []

    @pynvim.function('GetFileContents', sync=True)
    def getFileContents(self, args):
        buf = self.nvim.current.buffer
        pattern = re.compile(r'^\s*\s\*\s\[.+\]\((?P<dir>.+?)\)')
        dir_path = os.path.dirname(buf.name)
        directories = os.listdir(dir_path)
        appendedpattern = re.compile(r'\s\[\s\d+\s\]$')
        totalappendedpattern = re.compile(r'.*\s\[\s\d+\s\]$')

        if (self.toggle):
            for i in range(len(buf)):
                line = buf[i]
                m = pattern.match(line)
                a = totalappendedpattern.match(line)

                if (m and not a):
                    match_dir = m.group('dir')
                    match_dir_path = os.path.dirname(match_dir)
                    if (match_dir_path in directories):
                        match_dir_path_dirs = os.listdir(match_dir_path)
                        buf[i] += ' ' + \
                            '[ ' + str(len(match_dir_path_dirs)) + ' ]'
        else:
            for i in range(len(buf)):
                line = buf[i]
                buf[i] = re.sub(appendedpattern, '', line)

    @ pynvim.command('MemMachineToggle', nargs=0, range=None)
    def testcommand(self):
        self.toggle = not self.toggle
        self.nvim.command('call GetFileContents()')

    @ pynvim.autocmd('BufEnter', pattern='*.md', eval=None, sync=False)
    def on_vimwikienter(self):
        is_enabled = self.nvim.eval('g:MemMachineEnable')
        buf = self.nvim.current.buffer
        MemIndex = self.nvim.eval('g:MemMachineIndex')
        if (buf.name == MemIndex):
            if (is_enabled):
                self.toggle = True
            else:
                self.toggle = False
            self.nvim.command('call GetFileContents()')
