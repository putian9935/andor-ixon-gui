import numpy as np
import matplotlib.pyplot as plt 
import asyncio 


class Plotter:
    def __init__(self, x) -> None:
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title('Andor Camera')
        self.x = x
        self.axes_image = plt.imshow(np.lib.stride_tricks.as_strided(x, (1024, 1024), (2048,2), writeable=False)) 
        # this makes matplotlib window unclosable
        # plt.show (or plt.pause) overwrites the delete protocol
        # so this must be called first 
        plt.show(block=False)
        self.fig.canvas.manager.window.protocol('WM_DELETE_WINDOW', lambda *_:print('Please close from the terminal!'))

    
    async def aupdate(self, rescale_cbar=True):
        while True:
            if rescale_cbar:
                self.axes_image.set_clim(np.min(self.x), np.max(self.x))
            self.axes_image.stale = True 
            self.fig.canvas.draw()
            await asyncio.sleep(0)
    
    def destroy(self):
        self.fig.canvas.manager.window.destroy()

        