import ctypes

k_handle = ctypes.WinDLL("Kernel32.dll")


PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False
dwProcessID = 0x5C0 #hex value of process id

response = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessID)

error = k_handle.GetLastError()

# print(error)
print(response)

