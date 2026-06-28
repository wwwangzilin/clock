import tkinter as tk
from ui.styles import BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT

class AppWindow(tk.Tk):
    """使用 Windows 11 原生窗口框架的 Tk 窗口"""
    def __init__(self):
        super().__init__()
        self.title("🍅 番茄钟")
        self.configure(bg=BG_COLOR)
        self._center_window()
        # 允许调整大小，但设置最小尺寸
        self.minsize(400, 400)
        self.resizable(True, True)

    def _center_window(self):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - WINDOW_WIDTH) // 2
        y = (sh - WINDOW_HEIGHT) // 2 - 30
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")