#https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw

import ctypes

user_handle = ctypes.WinDLL("User32.dll")
k_handle = ctypes.WinDLL("Kernel32.dll")

hWdn = None
lpText = "Hello world"
lpCaption = "Test Message Box"
uType = 0x00000001

response = user_handle.MessageBoxW(hWdn, lpText, lpCaption, uType)

error = k_handle.GetLastError()

if error != 0: # if above of 0, there will be an error
    print("Error code: {error}")
    exit(1)

if response == 1:
    print("Selected OK")
elif response == 2:
    print("Selected Cancel")