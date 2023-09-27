
# LookupPrivilegeValueW 


import ctypes

u_handle = ctypes.WinDLL("User32.dll")
k_handle = ctypes.WinDLL("Kernel32.dll")

# Token Access Rights
STANDARD_RIGHTS_REQUIRED = 0x000F0000
STANDARD_RIGHTS_READ = 0x00020000
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATION = 0x0004
TOKEN_QUERY = 0x0008
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_READ = (STANDARD_RIGHTS_READ | TOKEN_QUERY)
TOKEN_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | 
					TOKEN_ASSIGN_PRIMARY     |
					TOKEN_DUPLICATE          |
					TOKEN_IMPERSONATION      |
					TOKEN_QUERY              |
					TOKEN_QUERY_SOURCE       |
					TOKEN_ADJUST_PRIVILEGES  |
					TOKEN_ADJUST_GROUPS      |
					TOKEN_ADJUST_DEFAULT     |
					TOKEN_ADJUST_SESSIONID)



# access rights
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

# grab the windows name from User32
lpClassName = None
lpWindowName = ctypes.c_char_p(b"Untitled - Notepad")
# lpWindowName = ctypes.c_char_p(b"Administrator: Command Prompt")

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
if hProcess == 0:
    print(f"[ERROR] Could Not Grab Privilege Handle! Error code: {k_handle.GetLastError()}")
    exit(1)
else:
    print("[INFO] Privileged Handle Opened...")

### open process token is required when try to work with any of the tokens (like modify the token). 

ProcessHandle = hProcess # done from OpenProcess function 
DesiredAccess = TOKEN_ALL_ACCESS 
TokenHandle = ctypes.c_void_p() # C type void and it is empty pointer

response = k_handle.OpenProcessToken(ProcessHandle, DesiredAccess, ctypes.byref(TokenHandle)) # we use 'byref' cuz the parameter is a pointer 

if response > 0:
    print("[INFO] Got Handle!...") # means successfully able to open a handle to the access token inside of the "task manager" (if your target is task manager) process... we can look up the privileges we can modify whether it's enable or disable we can remove the privilege **cannot add privilege** 
else:
    print(f"[ERROR] Could Not Grab Privilege Token Handle! Error code: {k_handle.GetLastError()}")    

