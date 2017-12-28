# import ctypes

# class MEMORYSTATUSEX(ctypes.Structure):
    # _fields_ = [
        # ("dwLength", ctypes.c_ulong),
        # ("dwMemoryLoad", ctypes.c_ulong),
        # ("ullTotalPhys", ctypes.c_ulonglong),
        # ("ullAvailPhys", ctypes.c_ulonglong),
        # ("ullTotalPageFile", ctypes.c_ulonglong),
        # ("ullAvailPageFile", ctypes.c_ulonglong),
        # ("ullTotalVirtual", ctypes.c_ulonglong),
        # ("ullAvailVirtual", ctypes.c_ulonglong),
        # ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    # ]

    # def __init__(self):
        # # have to initialize this to the size of MEMORYSTATUSEX
        # self.dwLength = ctypes.sizeof(self)
        # super(MEMORYSTATUSEX, self).__init__()

# stat = MEMORYSTATUSEX()
# ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))

# print("MemoryLoad: %d%%" % (stat.dwMemoryLoad))

"""Functions for getting memory usage of Windows processes."""

__all__ = ['get_current_process', 'get_memory_info', 'get_memory_usage']

import ctypes
from ctypes import wintypes

GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = []
GetCurrentProcess.restype = wintypes.HANDLE

SIZE_T = ctypes.c_size_t

class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('PageFaultCount', wintypes.DWORD),
        ('PeakWorkingSetSize', SIZE_T),
        ('WorkingSetSize', SIZE_T),
        ('QuotaPeakPagedPoolUsage', SIZE_T),
        ('QuotaPagedPoolUsage', SIZE_T),
        ('QuotaPeakNonPagedPoolUsage', SIZE_T),
        ('QuotaNonPagedPoolUsage', SIZE_T),
        ('PagefileUsage', SIZE_T),
        ('PeakPagefileUsage', SIZE_T),
        ('PrivateUsage', SIZE_T),
    ]

GetProcessMemoryInfo = ctypes.windll.psapi.GetProcessMemoryInfo
GetProcessMemoryInfo.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX),
    wintypes.DWORD,
]
GetProcessMemoryInfo.restype = wintypes.BOOL

def get_current_process():
    """Return handle to current process."""
    return GetCurrentProcess()

def get_memory_info(process=None):
    """Return Win32 process memory counters structure as a dict."""
    if process is None:
        process = get_current_process()
    counters = PROCESS_MEMORY_COUNTERS_EX()
    ret = GetProcessMemoryInfo(process, ctypes.byref(counters),
                               ctypes.sizeof(counters))
    if not ret:
        raise ctypes.WinError()
    info = dict((name, getattr(counters, name))
                for name, _ in counters._fields_)
    return info

def get_memory_usage(process=None):
    """Return this process's memory usage in bytes."""
    info = get_memory_info(process=process)
    return info['PrivateUsage']

if __name__ == '__main__':
    import pprint
    pprint.pprint(get_memory_usage())
    pprint.pprint(get_memory_info())