import tkinter as tk
from tkinter import ttk
from ui.styles import BG_COLOR, TEXT_DARK, TEXT_LIGHT, BTN_START_BG, BTN_RESET_BG

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, timer, on_apply):
        super().__init__(parent)
        self.title("系统设置")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.geometry("300x220")
        self._center(parent)

        self.timer = timer
        self.on_apply = on_apply

        # 工作时长
        self.work_var = tk.IntVar(value=timer.work_min)
        self._add_scale("工作时长 (分)", self.work_var, 1, 60)

        # 短休息
        self.short_var = tk.IntVar(value=timer.short_break)
        self._add_scale("短休息 (分)", self.short_var, 1, 30)

        # 长休息
        self.long_var = tk.IntVar(value=timer.long_break)
        self._add_scale("长休息 (分)", self.long_var, 1, 60)

        # 按钮
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="应用", font=("Helvetica", 11),
                  bg=BTN_START_BG, fg=TEXT_DARK, relief="flat",
                  command=self._apply).pack(side="left", padx=5)
        tk.Button(btn_frame, text="取消", font=("Helvetica", 11),
                  bg=BTN_RESET_BG, fg="white", relief="flat",
                  command=self.destroy).pack(side="left", padx=5)

    def _add_scale(self, label, var, from_, to):
        frame = tk.Frame(self, bg=BG_COLOR)
        frame.pack(pady=5, padx=20, fill="x")
        tk.Label(frame, text=label, font=("Helvetica", 11), bg=BG_COLOR, fg=TEXT_DARK).pack(side="left")
        ttk.Scale(frame, from_=from_, to=to, variable=var, orient="horizontal", length=150).pack(side="right")

    def _apply(self):
        self.timer.adjust_times(work=self.work_var.get(),
                                short=self.short_var.get(),
                                long=self.long_var.get())
        self.on_apply()  # 通知主窗口刷新
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