import ctypes
from ctypes import wintypes
from ctypes.wintypes import DWORD, LONG

k_handle = ctypes.WinDLL('kernel32',use_last_error=True)

TH32CS_SNAPPROCESS = 0x2
ERROR_NO_MORE_FILES = 18

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", DWORD),
                ("cntUsage", DWORD),
                ("th32ProcessID", DWORD),
                ("th32DefaultHeapID", wintypes.LPARAM),
                ("th32ModuleID", DWORD),
                ("cntThreads", DWORD),
                ("th32ParentProcessID", DWORD),
                ("pcPriClassBase", LONG),
                ("dwFlags", DWORD),
                ("szExeFile", ctypes.c_char * 260)]
    



def findProc(procname):
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)

    k_handle.CreateToolhelp32Snapshot.argtypes = wintypes.DWORD,wintypes.DWORD
    k_handle.CreateToolhelp32Snapshot.restype = wintypes.HANDLE 
    k_handle.Process32First.argtypes = wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)
    k_handle.Process32First.restype = wintypes.BOOL
    k_handle.Process32Next.argtypes = wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)
    k_handle.Process32Next.restype = wintypes.BOOL


    hSnapshot = k_handle.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    if not k_handle.Process32First(hSnapshot, pe32):
        print('error:', ctypes.get_last_error())
        
                                         
    while True:
    
        if not k_handle.Process32Next(hSnapshot, pe32):
            err = ctypes.get_last_error()
            if err == ERROR_NO_MORE_FILES:
                break
            else:
                print('error:',err)
                
        if (pe32.szExeFile).decode('utf-8') == procname:
            return pe32.th32ProcessID


print(findProc("chrome.exe"))