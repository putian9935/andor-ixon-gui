from plotter import Plotter
import traceback
import asyncio
from andor_lib import *
from image import *

import logging
logging.basicConfig(filename='Example log', level=logging.INFO)

from contextlib import contextmanager 

class CamStatus:
    cam_temp = 100
    temp_code = None
    frame_cnt = 0
    status = None
    FPS = None
    fname = None


setup_backend()

plotter = Plotter(GetImageArray())


def error_catch(coro):
    async def ret(*args, **kwargs):
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except:
            traceback.print_exc()
    return ret


@error_catch
async def temp_monitor():
    while True:
        CamStatus.cam_temp, CamStatus.temp_code = GetTemperature()
        logging.info(f'Temperature {CamStatus.cam_temp}')
        logging.debug(f'Temp. code {CamStatus.temp_code}')
        await asyncio.sleep(1)


async def status_monitor():
    while True:
        CamStatus.status, _ = GetStatus()
        logging.info(f'Status {CamStatus.status}')
        await asyncio.sleep(1)


async def fps_monitor():
    last_cnt = CamStatus.frame_cnt
    while True:
        CamStatus.FPS = CamStatus.frame_cnt - last_cnt
        logging.info(f'FPS: {CamStatus.FPS}')
        last_cnt = CamStatus.frame_cnt
        await asyncio.sleep(1)


@error_catch
async def wait_until_temperature_above(temp):
    while CamStatus.cam_temp < temp:
        await asyncio.sleep(1)


@error_catch
async def wait_until_temperature_stabilized():
    while CamStatus.temp_code != 20036:
        await asyncio.sleep(1)


# @error_catch
async def wait_until_temperature_is(temp):
    while CamStatus.cam_temp != temp:
        await asyncio.sleep(1)


async def fast_get():
    GetMostRecentImage16()
    CamStatus.frame_cnt += 1
    await asyncio.sleep(0)


async def wait_acq():
    await asyncio.get_event_loop().run_in_executor(None, WaitForAcquisition)
    GetMostRecentImage16()
    CamStatus.frame_cnt += 1

def spool_check(spool, get_fname : callable):
    if spool:
        if get_fname is None:
            logging.error('fname is None!')
            raise ValueError("fname is None!")
        try:
            fn = get_fname()
        except:
            traceback.print_exc()
            return 
        CamStatus.fname = fn
        TurnOnSpool(fn)
    return True 


@contextmanager 
def set_acquisition(acq_mode, trig_mode, kcc=0, exposure_time=1e-3, num_kin=1, read_mode=4, emccd_gain=0):
    try: 
        assert GetStatus()[0] == 20073
        SetAcquisitionMode(acq_mode)# run until abort
        SetReadMode(read_mode)  # image
        SetTriggerMode(trig_mode)  # internal
        SetExposureTime(exposure_time)  # exposure time
        SetKineticCycleTime(kcc)
        SetNumberKinetics(num_kin)
        SetEMCCDGain(emccd_gain)
        # TTL high, Perm Open, close, open, Perm open (Ext)
        SetShutterEx(1, 1, 0, 0, 1)
        yield
    except asyncio.CancelledError:
        pass
    except:
        traceback.print_exc()
    finally:
        AbortAcquisition()

async def real_time(spool=False, get_fname=None):
    if not spool_check(spool, get_fname):
        return 
    with set_acquisition(5, 0):
        StartAcquisition()
        while True:
            await fast_get()



async def external_trig(spool=False, get_fname=None):
    if not spool_check(spool, get_fname):
        return 
    with set_acquisition(5, 1):
        StartAcquisition()
        while True:
            await wait_acq()


async def external_start(spool=False, get_fname=None):
    num_kin = 2
    with set_acquisition(3, 6, 0.05, 1e-3, num_kin):
        while True:
            if not spool_check(spool, get_fname):
                break
            assert StartAcquisition() == SUCCESS
            for _ in range(num_kin):
                await wait_acq()


def init_cam():
    cam_cnt = GetAvailableCamera()[0]
    if cam_cnt != 1:
        raise ValueError(
            "In correct camera count: cam_cnt != 1. Did you\n1. forget to turn on or connect the camera;\n2. have another Andor software running.")

    assert Initialize() == SUCCESS
    SetFanMode(0)  # high
    CoolerON() 
    SetTemperature(-60) 

    SetVSSpeed(1) # [1.13]
    SetOutputAmplifier(0)   # electron multiplication
    SetHSSpeed(0, 0)   # 30MHz
    SetPreAmpGain(1)  # Pre amp gain 2
    SetBaselineClamp(1)   # Baseline clamp ON

    SetImage(1, 1, 1, 1024, 1, 1024)  # full image


async def shutdown_cam():
    print("Cleaning up...")
    CoolerOFF()
    task = asyncio.create_task(temp_monitor())
    print("Waiting for temperature going above -20C")
    await wait_until_temperature_above(-20)
    task.cancel()
    ShutDown() 


if __name__ == '__main__':
    async def main():
        backgrounds = [
            asyncio.create_task(temp_monitor()),
            asyncio.create_task(status_monitor()),
            asyncio.create_task(plotter.aupdate())]
        try:
            # await wait_until_temperature_is(0)
            await real_time()
            # await external_trig()
            # await external_start(True, 'test_external.fits')
        except (KeyboardInterrupt, asyncio.CancelledError):
            for bg in backgrounds:
                if not bg.done() and not bg.cancelled():
                    bg.cancel()
    init_cam()
    asyncio.run(main())
    shutdown_cam()
