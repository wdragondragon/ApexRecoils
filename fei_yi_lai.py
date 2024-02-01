# -*- coding: cp936 -*-
import ctypes
import time

if __name__ == '__main__':
    objdll = ctypes.cdll.LoadLibrary(r".\msdk.dll")
    # 定义函数原型
    M_Open = objdll.M_Open
    M_Open.argtypes = [ctypes.c_int]
    M_Open.restype = ctypes.c_void_p

    M_Open_VidPid = objdll.M_Open_VidPid
    M_Open_VidPid.argtypes = [ctypes.c_int, ctypes.c_int]
    M_Open_VidPid.restype = ctypes.c_void_p

    M_KeyPress = objdll.M_KeyPress
    M_KeyPress.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    M_KeyPress.restype = ctypes.c_int

    M_Close = objdll.M_Close
    M_Close.argtypes = [ctypes.c_void_p]
    M_Close.restype = ctypes.c_int
    hdl = objdll.M_Open_VidPid(0xC216, 0x0102)
    print(hdl)
    time.sleep(1)
    # objdll.M_KeyPress(ctypes.c_void_p(hdl), ctypes.c_int(6), ctypes.c_int(1))
    objdll.M_KeyPress(hdl, 6, 1)
    # objdll.M_KeyUp(hdl, 4)
    objdll.M_Close(hdl)
