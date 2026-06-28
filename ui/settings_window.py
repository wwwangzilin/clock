import tkinter as tk
from tkinter import ttk
import sv_ttk
from ui.styles import BG_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT, CARD_COLOR

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, timer, on_apply):
        super().__init__(parent)
        self.title("系统设置")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.geometry("320x260")
        sv_ttk.set_theme("light")
        self._center(parent)

        self.timer = timer
        self.on_apply = on_apply

        # 内容容器
        container = tk.Frame(self, bg=CARD_COLOR,
                             highlightbackground="#e0e0e0", highlightthickness=1)
        container.pack(padx=20, pady=(16, 8), fill="both", expand=True)

        # 工作时长
        self.work_var = tk.IntVar(value=timer.work_min)
        self._add_row(container, "工作时长 (分)", self.work_var, 1, 120)

        # 短休息
        self.short_var = tk.IntVar(value=timer.short_break)
        self._add_row(container, "短休息 (分)", self.short_var, 1, 30)

        # 长休息
        self.long_var = tk.IntVar(value=timer.long_break)
        self._add_row(container, "长休息 (分)", self.long_var, 1, 60)

        # 按钮
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=(4, 16))
        ttk.Button(btn_frame, text="✓ 应用", style="Primary.TButton",
                   command=self._apply).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="✕ 取消", style="Secondary.TButton",
                   command=self.destroy).pack(side="left", padx=4)

    def _add_row(self, parent, label, var, from_, to):
        frame = tk.Frame(parent, bg=CARD_COLOR)
        frame.pack(pady=8, padx=16, fill="x")
        tk.Label(frame, text=label, font=("Segoe UI", 11),
                 bg=CARD_COLOR, fg=TEXT_PRIMARY).pack(side="left")
        # Spinbox 替代 Scale，更精确
        sb = ttk.Spinbox(
            frame, from_=from_, to=to,
            textvariable=var, width=4,
            font=("Segoe UI", 11),
        )
        sb.pack(side="right")

    def _apply(self):
        self.timer.adjust_times(work=self.work_var.get(),
                                short=self.short_var.get(),
                                long=self.long_var.get())
        self.on_apply()
        self.destroy()

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")