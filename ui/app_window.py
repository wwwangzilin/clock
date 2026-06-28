import tkinter as tk
from ui.styles import BG_COLOR, TITLE_BG, TEXT_DARK, WINDOW_WIDTH, WINDOW_HEIGHT

class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # 无边框
        self.configure(bg=BG_COLOR)
        self._center_window()
        self._create_title_bar()
        self._bind_drag()

    def _center_window(self):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - WINDOW_WIDTH) // 2
        y = (sh - WINDOW_HEIGHT) // 2 - 30
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def _create_title_bar(self):
        self.title_canvas = tk.Canvas(self, bg=BG_COLOR, height=40, highlightthickness=0)
        self.title_canvas.pack(fill="x")

        # 圆角标题栏背景
        w = WINDOW_WIDTH
        r = 18
        self.title_canvas.create_polygon(
            r, 4, w - r, 4, w - 4, r, w - 4, 36 - r,
            w - r, 36, r, 36, 4, 36 - r, 4, r,
            fill=TITLE_BG, outline="", smooth=True)

        # 标题文字（保存 ID，方便后续调整位置）
        self.title_text_id = self.title_canvas.create_text(
            20, 20, anchor="w", text="🍅 番茄钟",
            font=("Helvetica", 12, "bold"), fill=TEXT_DARK)

        # 关闭按钮
        self.close_btn_id = self.title_canvas.create_text(
            WINDOW_WIDTH - 20, 20, anchor="e", text="✕",
            font=("Helvetica", 14), fill=TEXT_DARK)
        self.title_canvas.tag_bind(self.close_btn_id, "<Enter>",
                                   lambda e: self.title_canvas.itemconfig(self.close_btn_id, fill="red"))
        self.title_canvas.tag_bind(self.close_btn_id, "<Leave>",
                                   lambda e: self.title_canvas.itemconfig(self.close_btn_id, fill=TEXT_DARK))
        self.title_canvas.tag_bind(self.close_btn_id, "<Button-1>", lambda e: self.destroy())

    def _bind_drag(self):
        self.title_canvas.bind("<Button-1>", self._start_move)
        self.title_canvas.bind("<B1-Motion>", self._on_move)

    def _start_move(self, event):
        self._x = event.x
        self._y = event.y

    def _on_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")