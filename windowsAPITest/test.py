import ctypes

# from ctypes import wintypes

# ULONG_PTR = wintypes.LPARAM  # ULONG_PTR type changes size 32-/64-bit.  LPARAM does too.
# MAX_PATH = 260               # Needed for "exe" array to define correctly
# TH32CS_SNAPPROCESS = 0x2
# ERROR_NO_MORE_FILES = 18

# # Use the wide version of the structure with Python to get Unicode strings for "exe"
# class PROCESSENTRY32W(ctypes.Structure):
#     _fields_ = [('size', wintypes.DWORD),
#                 ('usage', wintypes.DWORD),
#                 ('pid', wintypes.DWORD),
#                 ('heap', ULONG_PTR),          # Use correct type for 32-/64-bit
#                 ('mid', wintypes.DWORD),
#                 ('threads', wintypes.DWORD),
#                 ('ppid', wintypes.DWORD),
#                 ('pri', wintypes.LONG),
#                 ('flags', wintypes.DWORD),
#                 ('exe', wintypes.WCHAR * MAX_PATH)]  # Correct way to declare array

# entry = PROCESSENTRY32W()
# entry.size = ctypes.sizeof(PROCESSENTRY32W)

# dll = ctypes.WinDLL('kernel32',use_last_error=True)  # Ensures capturing last error

# # Declaring parameter types and return values helps catch errors.
# # HANDLE is different on 32-/64-bit as well and can get truncated.
# dll.CreateToolhelp32Snapshot.argtypes = wintypes.DWORD,wintypes.DWORD
# dll.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
# dll.Process32FirstW.argtypes = wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)
# dll.Process32FirstW.restype = wintypes.BOOL
# dll.Process32NextW.argtypes = wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)
# dll.Process32NextW.restype = wintypes.BOOL

# snapshot = dll.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
# if not dll.Process32FirstW(snapshot, entry):
#     print('error:', ctypes.get_last_error()) # gets error captured by ctypes call
# else:                                        # not last Win32 call in general.
#     print(entry.exe)

# while True:
#     if not dll.Process32NextW(snapshot, entry):
#         err = ctypes.get_last_error()
#         if err == ERROR_NO_MORE_FILES:
#             break
#         else:
#             print('error:',err)
#     print(entry.exe)


# print(ctypes.sizeof([1,2,3]))

# nBytes = ctypes.c_int(100)
# print(type(nBytes))


a = ctypes.create_string_buffer(b'', len("Hello world"))
print(a)