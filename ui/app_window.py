import tkinter as tk
import ctypes
from ctypes import wintypes
from ui.styles import BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, scale_size


def _enable_acrylic(hwnd):
    """为窗口启用 Windows 11 亚克力（高斯模糊）背景效果"""
    try:
        dwmapi = ctypes.windll.dwmapi
        # DWMWA_SYSTEMBACKDROP_TYPE = 38 (Windows 11 22523+)
        #   2 = Mica,  3 = Acrylic,  4 = Tabbed (Mica Alt)
        backdrop_type = wintypes.INT(3)  # Acrylic
        dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            wintypes.UINT(38),  # DWMWA_SYSTEMBACKDROP_TYPE
            ctypes.byref(backdrop_type),
            ctypes.sizeof(wintypes.INT),
        )
        return True
    except Exception:
        pass

    # 降级：Windows 10 毛玻璃效果
    try:
        dwmapi = ctypes.windll.dwmapi
        # DWMWA_USE_HOSTBACKDROPBRUSH = 17
        backdrop = wintypes.INT(1)
        dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            wintypes.UINT(17),
            ctypes.byref(backdrop),
            ctypes.sizeof(wintypes.INT),
        )
        return True
    except Exception:
        return False


class AppWindow(tk.Tk):
    """Windows 11 原生窗口 + 亚克力模糊背景"""
    def __init__(self):
        super().__init__()
        self.title("🍅 番茄钟")
        self.configure(bg=BG_COLOR)

        # 启用亚克力模糊
        _enable_acrylic(self.winfo_id())

        # DPI 感知窗口缩放
        scale = scale_size(1)
        w = int(WINDOW_WIDTH * scale)
        h = int(WINDOW_HEIGHT * scale)
        self._center_window(w, h)

        # 允许调整大小，但设置最小尺寸
        self.minsize(int(400 * scale), int(400 * scale))
        self.resizable(True, True)

    def _center_window(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2 - 30
        self.geometry(f"{w}x{h}+{x}+{y}")