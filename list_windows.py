import ctypes
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

windows = []

def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            windows.append((hwnd, buff.value))
    return True

EnumWindows(EnumWindowsProc(foreach_window), 0)

print(f"Total visible windows: {len(windows)}")
for hwnd, title in windows:
    if any(k in title.lower() for k in ["spotify", "edge", "chrome", "podcast", "creator"]):
        print(f"  [HWND {hwnd}] {title}")
