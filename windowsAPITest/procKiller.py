import ctypes

u_handle = ctypes.WinDLL("User32.dll")
k_handle = ctypes.WinDLL("Kernel32.dll")

# access rights
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF) # https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights#:~:text=Meaning-,PROCESS_ALL_ACCESS,-(STANDARD_RIGHTS_REQUIRED%20(0x000F0000L)%20%7C%20SYNCHRONIZE


# grab the windows name from User32
lpClassName = None
lpWindowName = ctypes.c_char_p(b"Untitled - Notepad")

# grab the handler of the process
hWnd = u_handle.FindWindowA(lpClassName, lpWindowName)

# check error
if hWnd == 0:
    print(f"[ERROR] Could Not Grab Handler! Error code: {k_handle.GetLastError()}")
    exit(1)
else:
    print("[INFO] Grabbed Handler...")

# get the PID of the process at the handle
lpdwProcessId = ctypes.c_ulong() # same as DWORD


# use byte to pass a pointer to the value as need by the API call
response = u_handle.GetWindowThreadProcessId(hWnd, ctypes.byref(lpdwProcessId))

# check error
if response == 0:
    print(f"[ERROR] Could Not Get PID form Handle! Error code: {k_handle.GetLastError()}")
    exit(1)
else:
    print("[INFO] Found PID...")


# opening the process by PID with specific access
dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False
dwProcessID = lpdwProcessId #hex value of process id

# calling the win api to open the process
hProcess = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessID)

# check error
if response == 0:
    print(f"[ERROR] Could Not Grab Privilege Handle! Error code: {k_handle.GetLastError()}")
    exit(1)
else:
    print("[INFO] Privileged Handle Opened...")


uExitCode = 0x1

# kill the process
response = k_handle.TerminateProcess(hProcess, uExitCode)

# check error
if response == 0:
    print(f"[ERROR] Could Not Kill The Process! Error code: {k_handle.GetLastError()}")
    exit(1)
else:
    print(f"[INFO] Process Killed...")