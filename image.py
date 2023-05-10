import numpy as np 
from ctypes import *
import matplotlib as mpl 
import matplotlib.pyplot as plt

def setup_backend():
    mpl.use('TkAgg')

def prepare_image(x : np.ndarray):
    return axes_image 

def update_image(axes_image):
    axes_image.stale = True
    plt.pause(1e-3)


if __name__ == '__main__':
    # prepare an image 
    x = np.zeros(1024*1024, dtype=np.uint16)
    p = x.ctypes.data_as(POINTER(c_uint16))
    p[3] = 6

    setup_backend()    
    axes_image = prepare_image(x)

    import time 
    tt = time.perf_counter()
    for i in range(1000):
        p[np.random.randint(0,1024*1024-1)] = np.random.randint(0,6)  # write to x randomly
        update_image(axes_image)
        plt.pause(1e-2)
    print(time.perf_counter() - tt)