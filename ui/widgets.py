import tkinter as tk
from ui.styles import (
    SETTING_BG, TEXT_LIGHT, TEXT_DARK, CARD_COLOR, WORK_COLOR, CARD_RADIUS, BG_COLOR
)

class RoundedCard(tk.Canvas):
    """圆角卡片，用于显示计时器数字"""
    def __init__(self, parent, width, height, radius=CARD_RADIUS, **kwargs):
        super().__init__(parent, bg=BG_COLOR, height=height, highlightthickness=0, **kwargs)
        self.radius = radius
        self.card_bg = None
        self.timer_text_id = None
        self.bind("<Configure>", self._on_resize)

    def set_text(self, text, color=WORK_COLOR):
        if self.timer_text_id is None:
            self.timer_text_id = self.create_text(
                self.winfo_reqwidth() // 2, self.winfo_reqheight() // 2,
                text=text, font=("Helvetica", 58, "bold"), fill=color)
        else:
            self.itemconfig(self.timer_text_id, text=text, fill=color)

    def _on_resize(self, event):
        self.delete("card_bg")
        w, h = event.width, event.height
        r = self.radius
        self.create_polygon(
            r, 4, w - r, 4, w - 4, r, w - 4, h - r,
            w - r, h, r, h, 4, h - r, 4, r,
            fill=CARD_COLOR, outline="#e0e0e0", smooth=True, tags="card_bg")
        if self.timer_text_id:
            self.coords(self.timer_text_id, w // 2, h // 2)
            self.tag_raise(self.timer_text_id)

class TimeAdjuster(tk.Frame):
    """时长调节器：标签 + [-] 数字 [+]"""
    def __init__(self, parent, label_text, var, time_type, on_adjust, **kwargs):
        super().__init__(parent, bg=SETTING_BG, **kwargs)
        self.var = var
        self.time_type = time_type
        self.on_adjust = on_adjust

        lbl = tk.Label(self, text=label_text, font=("Helvetica", 9), fg=TEXT_LIGHT, bg=SETTING_BG)
        lbl.pack()

        inner = tk.Frame(self, bg=SETTING_BG)
        inner.pack()

        btn_minus = tk.Button(inner, text="−", font=("Helvetica", 10, "bold"),
                              width=2, relief="flat", bg="#e0d5c1", activebackground="#d4c9b5",
                              command=lambda: self._adjust(-1))
        btn_minus.pack(side="left")

        val_label = tk.Label(inner, textvariable=var, font=("Helvetica", 12, "bold"),
                             fg=TEXT_DARK, bg=SETTING_BG, width=3)
        val_label.pack(side="left")

        btn_plus = tk.Button(inner, text="+", font=("Helvetica", 10, "bold"),
                             width=2, relief="flat", bg="#e0d5c1", activebackground="#d4c9b5",
                             command=lambda: self._adjust(1))
        btn_plus.pack(side="left")

    def _adjust(self, delta):
        new_val = self.var.get() + delta
        if 1 <= new_val <= 120:
            self.var.set(new_val)
            self.on_adjust(self.time_type, new_val)