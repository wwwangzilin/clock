import tkinter as tk
from tkinter import ttk
from ui.styles import (
    TEXT_SECONDARY, TEXT_PRIMARY, CARD_COLOR, BG_COLOR, ACCENT
)

class TimerCard(tk.Frame):
    """Windows 11 风格的计时卡片（白色圆角卡片，显示大号时间）"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=CARD_COLOR, **kwargs)
        self._create_shadow()

        # 时间标签
        self.time_label = tk.Label(
            self,
            text="25:00",
            font=("Segoe UI", 64, "bold"),
            fg=ACCENT,
            bg=CARD_COLOR,
        )
        self.time_label.pack(expand=True, fill="both", pady=(40, 10))

        # 阶段标签
        self.status_label = tk.Label(
            self,
            text="点击下方按钮开始专注",
            font=("Segoe UI", 11),
            fg=TEXT_SECONDARY,
            bg=CARD_COLOR,
        )
        self.status_label.pack(pady=(0, 30))

    def _create_shadow(self):
        """用边框模拟 Windows 11 的卡片阴影效果"""
        self.configure(highlightbackground="#e0e0e0", highlightthickness=1, highlightcolor="#e0e0e0")

    def set_time(self, text, color=ACCENT):
        self.time_label.config(text=text, fg=color)

    def set_status(self, text):
        self.status_label.config(text=text)


class TimeAdjuster(tk.Frame):
    """Windows 11 风格的时间调节器"""
    def __init__(self, parent, label_text, var, time_type, on_adjust, **kwargs):
        super().__init__(parent, bg=BG_COLOR, **kwargs)
        self.var = var
        self.time_type = time_type
        self.on_adjust = on_adjust

        lbl = tk.Label(
            self, text=label_text,
            font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_COLOR
        )
        lbl.pack(anchor="center")

        inner = tk.Frame(self, bg=BG_COLOR)
        inner.pack(anchor="center")

        btn_minus = tk.Button(
            inner, text="−", font=("Segoe UI", 12, "bold"),
            width=2, relief="flat", bg="#e8e8e8", fg=TEXT_PRIMARY,
            activebackground="#d0d0d0", cursor="hand2",
            bd=0, padx=8, pady=2,
            command=lambda: self._adjust(-1)
        )
        btn_minus.pack(side="left", padx=2)

        val_label = tk.Label(
            inner, textvariable=var,
            font=("Segoe UI", 14, "bold"),
            fg=TEXT_PRIMARY, bg=BG_COLOR, width=3
        )
        val_label.pack(side="left", padx=4)

        btn_plus = tk.Button(
            inner, text="+", font=("Segoe UI", 12, "bold"),
            width=2, relief="flat", bg="#e8e8e8", fg=TEXT_PRIMARY,
            activebackground="#d0d0d0", cursor="hand2",
            bd=0, padx=8, pady=2,
            command=lambda: self._adjust(1)
        )
        btn_plus.pack(side="left", padx=2)

    def _adjust(self, delta):
        new_val = self.var.get() + delta
        if 1 <= new_val <= 120:
            self.var.set(new_val)
            self.on_adjust(self.time_type, new_val)