from tkinter import *
import asyncio
from cam_wrapper import init_cam, shutdown_cam, real_time, external_trig, temp_monitor, status_monitor, fps_monitor, plotter, external_start, CamStatus
from common_feeder import get_name_from_file, get_name_from_time


class MyTk(Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.task = [
            asyncio.create_task(self.aupdate()),
            asyncio.create_task(temp_monitor()),
            asyncio.create_task(status_monitor()),
            asyncio.create_task(plotter.aupdate()),
            asyncio.create_task(fps_monitor()),
        ]
        self.spooling = IntVar(self)
        self.job = None

    async def aupdate(self):
        """ the Tk loop """
        while True:
            self.update()
            try:
                await asyncio.sleep(0)
            except:
                return

    def close(self):
        if self.job:
            self.job.cancel()
        for t in self.task:
            if not t.cancelled() and not t.done():
                t.cancel()
        plotter.destroy()
        self.destroy()


modes = {'internal': real_time, 'external': external_trig,
         'external start': external_start}


def draw_tk():
    # Create an instance of Tkinter frame or window
    win = MyTk()

    enable_spool = Checkbutton(
        win, text='Enable spooling', font=(None, 12), state=DISABLED, variable=win.spooling, onvalue=1, offvalue=0)
    enable_spool.grid(row=1, columnspan=4, sticky=W)

    def stop():
        if not win.job:
            return
        win.job.cancel()
        enable_spool['state'] = ACTIVE

    def start(key: str):
        def ret():
            stop()
            enable_spool['state'] = DISABLED
            if win.spooling.get():
                win.job = asyncio.create_task(
                    modes[key](True, get_name_from_time))
            else:
                win.job = asyncio.create_task(modes[key]())
        return ret

    # Set title of tkinter frame
    win.title('Andor Camera Terminal')

    buttons = [
        Button(win, text='Internal', font=(None, 14),
               command=start('internal'), state=DISABLED),
        Button(win, text='External', font=(None, 14),
               command=start('external'), state=DISABLED),
        Button(win, text='External start', font=(None, 14),
               command=start('external start'), state=DISABLED),
        Button(win, text='Stop', font=(None, 14), command=stop),
    ]
    for i, b in enumerate(buttons):
        b.grid(row=0, column=i, sticky=NSEW)

    banners = [Label(win, font=(None, 10,)) for _ in range(5)]
    for i, b in enumerate(banners):
        b.grid(row=i+2, columnspan=4, sticky=W)

    async def update_banner():
        while True:
            if not CamStatus.status:
                banners[0]['text'] = 'Initializing camera...'
                banners[1]['text'] = ''
                banners[2]['text'] = ''
                banners[3]['text'] = ''
            else:
                banners[0]['text'] = f'Current Temperature: {CamStatus.cam_temp}'
                banners[1]['text'] = f'FPS: {CamStatus.FPS}'
                banners[2]['text'] = f'Last spooling file name: {CamStatus.fname}'
                banners[3]['text'] = f'Temp code: {CamStatus.temp_code}'
                banners[4]['text'] = f'Status code: {CamStatus.status}'
            await asyncio.sleep(1)

    async def update_clickables():
        while not CamStatus.status:
            await asyncio.sleep(.2)
        for b in buttons:
            b['state'] = ACTIVE
        enable_spool['state'] = ACTIVE
    win.task.append(asyncio.create_task(update_banner()))
    win.task.append(asyncio.create_task(update_clickables()))
    return win


async def main():
    win = draw_tk()
    await asyncio.get_event_loop().run_in_executor(None, init_cam)
    # wait gui close
    await win.task[0]
    await shutdown_cam()


asyncio.run(main())
