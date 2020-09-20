import pynvim


@pynvim.plugin
class Main(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False

    @pynvim.function('GetFileContents', sync=True)
    def getFileContents(self, args):
        for i in range(len(self.nvim.current.buffer)):
            self.nvim.current.buffer[i] += str(
                len(self.nvim.current.buffer[i]))

    @pynvim.command('MemMachToggle', nargs=0, range=None)
    def testcommand(self):
        self.toggle = not self.toggle
        if (self.toggle):
            self.nvim.command('call GetFileContents()')
        # TODO: Untoggle should remove all the added info

    @ pynvim.autocmd('BufEnter', pattern='*.md', eval=None, sync=False)
    def on_vimwikienter(self):
        if (self.toggle == True):
            # TODO: Check if file is a vimwiki filetype
            self.nvim.command('call GetFileContents()')
