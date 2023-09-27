import ctypes

from ctypes.wintypes import DWORD, LPSTR, WORD, HANDLE, LPBYTE

k_handle = ctypes.WinDLL("Kernel32.dll")
CREATE_NEW_CONSOLE = 0x00000010


# structure of process info
class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPSTR),
        ("lpDesktop", LPSTR),
        ("lpTitle", LPSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput",HANDLE),
        ("hStdError", HANDLE)
    ]
    
# structure for process info 
class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD)
    ]
    
lpApplicationName = "C:\\Windows\\System32\\cmd.exe"
lpCommandLine = None 
lpProcessAttributes = None
lpThreadAttributes = None
lpEnvironment = None
lpCurrentDirectory = None

dwCreationFlags = 0x00000010 # create new console
bInheritHandles = False
lpProcessInformation = PROCESS_INFORMATION() # pointer to the process information struct accourding to docs
lpStartupInfo = STARTUPINFO()
lpStartupInfo.wShowWindow = 0x1
lpStartupInfo.dwFlags = 0x1 #https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfoa#:~:text=contain%20additional%20information.-,STARTF_USESHOWWINDOW,-0x00000001


response = k_handle.CreateProcessW(
    lpApplicationName,
    lpCommandLine,
    lpProcessAttributes,
    lpThreadAttributes,
    bInheritHandles,
    dwCreationFlags,
    lpEnvironment,
    lpCurrentDirectory,
    ctypes.byref(lpStartupInfo), # pass reference
    ctypes.byref(lpProcessInformation)
    )

print(response)