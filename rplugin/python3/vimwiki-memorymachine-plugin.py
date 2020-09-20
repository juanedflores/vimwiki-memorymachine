import pynvim


@pynvim.plugin
class Main(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('GetFileContents', sync=True)
    def getFileContents(self, args):
        for i in range(len(self.nvim.current.buffer)):
            self.nvim.current.buffer[i] += str(
                len(self.nvim.current.buffer[i]))
