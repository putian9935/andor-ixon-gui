from ctypes import CDLL
from ctypes import *
import numpy as np
from os.path import splitext

wdll = CDLL(r"C:\Program Files\Andor SOLIS\atmcd64d_legacy.dll")
# wdll = CDLL(r"./atmcd64d_legacy_old.dll")
SUCCESS = 20002

def _GetAvailableCamera():
    f = wdll.GetAvailableCameras
    f.argtypes = [POINTER(c_long)]
    f.restype = c_uint32

    def ret():
        x = c_long()
        err = f(pointer(x))

        if err != 20002:
            raise RuntimeError("Error code: %d" % err)
        return x.value, err
    return ret


def _Initialize():
    f = wdll.Initialize
    f.argtypes = [POINTER(c_char)]
    f.restype = c_uint32

    def ret():
        return f(r"C:\Program Files\Andor SOLIS".encode())
    return ret


def _ShutDown():
    f = wdll.ShutDown
    f.restype = c_uint32

    def ret():
        return f()
    return ret


def _SetTemperature():
    f = wdll.SetTemperature
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(temp):
        return f(temp)
    return ret


def _GetTemperature():
    f = wdll.GetTemperature
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        temp = c_int()
        err = f(pointer(temp))
        return temp.value, err
    return ret


def _CoolerON():
    f = wdll.CoolerON
    f.restype = c_uint32

    def ret():
        return f()
    return ret


def _CoolerOFF():
    f = wdll.CoolerOFF
    f.restype = c_uint32

    def ret():
        return f()
    return ret


def _SetFanMode():
    f = wdll.SetFanMode
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(fan_mode):
        err = f(fan_mode)
        return err
    return ret


def _GetNumberVSSpeeds():
    f = wdll.GetNumberVSSpeeds
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        speeds = c_int()
        err = f(pointer(speeds))
        return speeds.value, err
    return ret


def _GetVSSpeed():
    f = wdll.GetVSSpeed
    f.argtypes = [c_int, POINTER(c_float)]
    f.restype = c_uint32

    def ret(index):
        speed = c_float()
        err = f(index, pointer(speed))
        return speed.value, err
    return ret


def _SetVSSpeed():
    f = wdll.SetVSSpeed
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(index):
        err = f(index)
        return err
    return ret


def _GetFastestRecommendedVSSpeed():
    f = wdll.GetFastestRecommendedVSSpeed
    f.argtypes = [POINTER(c_int), POINTER(c_float)]
    f.restype = c_uint32

    def ret():
        index = c_int()
        speed = c_float()
        err = f(pointer(index), pointer(speed))
        return index, speed, err
    return ret


def _GetNumberVSSpeeds():
    f = wdll.GetNumberVSSpeeds
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        speeds = c_int()
        err = f(pointer(speeds))
        return speeds.value, err
    return ret


def _GetVSSpeed():
    f = wdll.GetVSSpeed
    f.argtypes = [c_int, POINTER(c_float)]
    f.restype = c_uint32

    def ret(index):
        speed = c_float()
        err = f(index, pointer(speed))
        return speed.value, err
    return ret


def _SetVSSpeed():
    f = wdll.SetVSSpeed
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(index):
        err = f(index)
        return err
    return ret


def _GetNumberADChannels():
    f = wdll.GetNumberADChannels
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        channels = c_int()
        err = f(pointer(channels))
        return channels.value, err
    return ret


def _GetNumberAmp():
    f = wdll.GetNumberAmp
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        amp = c_int()
        err = f(pointer(amp))
        return amp.value, err
    return ret


def _GetBitDepth():
    f = wdll.GetBitDepth
    f.argtypes = [c_int, POINTER(c_int)]
    f.restype = c_uint32

    def ret(channel):
        depth = c_int()
        err = f(channel, pointer(depth))
        return depth.value, err
    return ret


def _SetOutputAmplifier():
    f = wdll.SetOutputAmplifier
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(typ):
        err = f(typ)
        return err
    return ret


def _GetNumberHSSpeeds():
    f = wdll.GetNumberHSSpeeds
    f.argtypes = [c_int, c_int, POINTER(c_int)]
    f.restype = c_uint32

    def ret(channel, typ):
        speeds = c_int()
        err = f(channel, typ, pointer(speeds))
        return speeds.value, err
    return ret


def _GetHSSpeed():
    f = wdll.GetHSSpeed
    f.argtypes = [c_int, c_int, c_int, POINTER(c_float)]
    f.restype = c_uint32

    def ret(channel, typ, index):
        speed = c_float()
        err = f(channel, typ, index, pointer(speed))
        return speed.value, err
    return ret


def _SetHSSpeed():
    f = wdll.SetHSSpeed
    f.argtypes = [c_int, c_int]
    f.restype = c_uint32

    def ret(typ, index):
        err = f(typ, index)
        return err
    return ret


def _GetNumberPreAmpGains():
    f = wdll.GetNumberPreAmpGains
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        no_gains = c_int()
        err = f(pointer(no_gains))
        return no_gains.value, err
    return ret


def _GetPreAmpGain():
    f = wdll.GetPreAmpGain
    f.argtypes = [c_int, POINTER(c_float)]
    f.restype = c_uint32

    def ret(index):
        gain = c_float()
        err = f(index, pointer(gain))
        return gain.value, err
    return ret


def _SetPreAmpGain():
    f = wdll.SetPreAmpGain
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(index):
        err = f(index)
        return err
    return ret

def _GetRegisterDump():
    f = wdll.GetRegisterDump
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        mode = c_int()
        err = f(pointer(mode))
        return mode.value, err
    return ret

def _SetRegisterDump():
    f = wdll.SetRegisterDump
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(mode):
        err = f(mode)
        return err
    return ret

def _SetReadoutRegisterPacking():
    f = wdll.SetReadoutRegisterPacking
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(mode):
        err = f(mode)
        return err
    return ret

def _SetAcquisitionMode():
    f = wdll.SetAcquisitionMode
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(mode):
        err = f(mode)
        return err
    return ret


def _SetShutterEx():
    f = wdll.SetShutterEx
    f.argtypes = [c_int, c_int, c_int, c_int, c_int]
    f.restype = c_uint32

    def ret(typ, mode, closingtime, openingtime, extmode):
        err = f(typ, mode, closingtime, openingtime, extmode)
        return err
    return ret


def _SetTriggerMode():
    f = wdll.SetTriggerMode
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(mode):
        err = f(mode)
        return err
    return ret


def _IsTriggerModeAvailable():
    f = wdll.IsTriggerModeAvailable
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(mode):
        err = f(mode)
        return err
    return ret


def _SetReadMode():
    f = wdll.SetReadMode
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(mode):
        err = f(mode)
        return err
    return ret


def _SetExposureTime():
    f = wdll.SetExposureTime
    f.argtypes = [c_float]
    f.restype = c_uint32

    def ret(time):
        err = f(time)
        return err
    return ret


def _SetKineticCycleTime():
    f = wdll.SetKineticCycleTime
    f.argtypes = [c_float]
    f.restype = c_uint32

    def ret(time):
        err = f(time)
        return err
    return ret

def _SetNumberKinetics():
    f = wdll.SetNumberKinetics
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(number):
        err = f(number)
        return err
    return ret


def _GetKeepCleanTime():
    f = wdll.GetKeepCleanTime
    f.argtypes = [POINTER(c_float)]
    f.restype = c_uint32

    def ret():
        KeepCleanTime = c_float()
        err = f(pointer(KeepCleanTime))
        return KeepCleanTime.value, err
    return ret


def _SetBaselineClamp():
    f = wdll.SetBaselineClamp
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(state):
        err = f(state)
        return err
    return ret


def _SetBaselineOffset():
    f = wdll.SetBaselineOffset
    f.argtypes = [c_int]
    f.restype = c_uint32

    def ret(offset):
        err = f(offset)
        return err
    return ret


def _StartAcquisition():
    f = wdll.StartAcquisition
    f.argtypes = []
    f.restype = c_uint32

    def ret():
        err = f()
        return err
    return ret


def _AbortAcquisition():
    f = wdll.AbortAcquisition
    f.restype = c_uint32

    def ret():
        err = f()
        return err
    return ret


def _WaitForAcquisition():
    f = wdll.WaitForAcquisition
    f.restype = c_uint32

    def ret():
        err = f()
        return err
    return ret


def _GetStatus():
    f = wdll.GetStatus
    f.argtypes = [POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        status = c_int()
        err = f(pointer(status))
        return status.value, err
    return ret


def _SetImage():
    f = wdll.SetImage
    f.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int]
    f.restype = c_uint32

    def ret(hbin, vbin, hstart, hend, vstart, vend):
        err = f(hbin, vbin, hstart, hend, vstart, vend)
        return err
    return ret


def _GetNumberAvailableImages():
    f = wdll.GetNumberAvailableImages
    f.argtypes = [POINTER(c_int), POINTER(c_int)]
    f.restype = c_uint32

    def ret():
        first = c_int()
        last = c_int()
        err = f(pointer(first), pointer(last))
        return first.value, last.value, err
    return ret


def _GetMostRecentImage16():
    f = wdll.GetMostRecentImage16
    f.argtypes = [POINTER(c_uint16)]

    f.restype = c_uint32
    img_buf = np.zeros(1024 * 1024, dtype=np.uint16)
    arr = img_buf.ctypes.data_as(POINTER(c_uint16))

    def ret():
        err = f(arr, c_uint(1024 * 1024))
        return img_buf, err
    def get_buf():
        return img_buf 
    return ret, get_buf  


def _GetMostRecentImage():
    f = wdll.GetMostRecentImage
    f.argtypes = [POINTER(c_uint32)]

    f.restype = c_uint32
    img_buf = np.zeros(1024 * 1024, dtype=np.uint32)
    arr = img_buf.ctypes.data_as(POINTER(c_uint32))

    def ret():
        err = f(arr, c_uint(1024 * 1024))
        return img_buf, err
    return ret


def _GetOldestImage():
    f = wdll.GetOldestImage
    f.argtypes = [POINTER(c_uint32)]
    f.restype = c_uint32
    img_buf = np.zeros(1024 * 1024, dtype=np.uint32)
    arr = img_buf.ctypes.data_as(POINTER(c_uint32))

    def ret():
        err = f(arr, c_uint(1024 * 1024))
        return img_buf, err
    return ret


def _GetImages():
    f = wdll.GetImages
    f.argtypes = [c_int, c_int, POINTER(
        c_int), c_uint, POINTER(c_uint), POINTER(c_uint)]

    f.restype = c_uint32
    img_buf = np.zeros(1024 * 1024 * 100, dtype=np.int32)
    arr = img_buf.ctypes.data_as(POINTER(c_int32))

    def ret(first, last):
        validfirst = c_uint()
        validlast = c_uint()
        err = f(first, last, arr, (1024*1024*(last-first+1)),
                pointer(validfirst), pointer(validlast))
        return img_buf, validfirst.value, validlast.value, err
    return ret


def _TurnOnSpool():
    f = wdll.SetSpool
    f.argtypes = [c_int, c_int,c_char_p, c_int]

    f.restype = c_uint32

    def ret(fname, buffersize=10):
        err = f(1, 5, splitext(fname)[0].encode(), buffersize)
        return err
    return ret

def _TurnOffSpool():
    f = wdll.SetSpool
    f.argtypes = [c_int, c_int,c_char_p, c_int]
    f.restype = c_uint32

    def ret():
        err = f(0, 0, "".encode(), 10)
        return err
    return ret

GetAvailableCamera = _GetAvailableCamera()
Initialize = _Initialize()
ShutDown = _ShutDown()

SetTemperature = _SetTemperature()
GetTemperature = _GetTemperature()
CoolerON = _CoolerON()
CoolerOFF = _CoolerOFF()
SetFanMode = _SetFanMode()

GetFastestRecommendedVSSpeed = _GetFastestRecommendedVSSpeed()
GetNumberVSSpeeds = _GetNumberVSSpeeds()
GetVSSpeed = _GetVSSpeed()
SetVSSpeed = _SetVSSpeed()
GetNumberADChannels = _GetNumberADChannels()  # returns 1 on iXon 888
GetNumberAmp = _GetNumberAmp()  # returns 2: electron multiplication / conventional
SetOutputAmplifier = _SetOutputAmplifier()
GetBitDepth = _GetBitDepth()  # returns 16

GetNumberHSSpeeds = _GetNumberHSSpeeds()
GetHSSpeed = _GetHSSpeed()
SetHSSpeed = _SetHSSpeed()

GetNumberPreAmpGains = _GetNumberPreAmpGains()
GetPreAmpGain = _GetPreAmpGain()
SetPreAmpGain = _SetPreAmpGain()

SetBaselineClamp = _SetBaselineClamp()
SetBaselineOffset = _SetBaselineOffset()

GetRegisterDump = _GetRegisterDump()
SetRegisterDump = _SetRegisterDump()
SetReadoutRegisterPacking = _SetReadoutRegisterPacking()

SetAcquisitionMode = _SetAcquisitionMode()
SetShutterEx = _SetShutterEx()
SetTriggerMode = _SetTriggerMode()
SetReadMode = _SetReadMode()
SetExposureTime = _SetExposureTime()
SetKineticCycleTime = _SetKineticCycleTime()
SetNumberKinetics = _SetNumberKinetics()
GetKeepCleanTime = _GetKeepCleanTime()
StartAcquisition = _StartAcquisition()
AbortAcquisition = _AbortAcquisition()
WaitForAcquisition = _WaitForAcquisition()
GetStatus = _GetStatus()

SetImage = _SetImage()
GetNumberAvailableImages = _GetNumberAvailableImages()
GetMostRecentImage16, GetImageArray = _GetMostRecentImage16()
GetMostRecentImage = _GetMostRecentImage()
GetOldestImage = _GetOldestImage()
GetImages = _GetImages()

TurnOnSpool = _TurnOnSpool()
TurnOffSpool = _TurnOffSpool()

# available mode 0,1,6,7,11
IsTriggerModeAvailable = _IsTriggerModeAvailable()


def show_all_vs_speed():
    for i in range(GetNumberVSSpeeds()[0]):
        print(GetVSSpeed(i))


def show_all_hs_speed(channel, typ):
    for i in range(GetNumberHSSpeeds(channel, typ)[0]):
        print(GetHSSpeed(channel, typ, i))


def show_all_pre_amp_gain():
    for i in range(GetNumberPreAmpGains()[0]):
        print(GetPreAmpGain(i))


if __name__ == '__main__':
    print(GetAvailableCamera())
    Initialize()
    SetTemperature(-60)
    CoolerON()
    import time
    for i in range(30):
        print(GetTemperature())
        time.sleep(1)
    CoolerOFF()
    ShutDown()
