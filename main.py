import tkinter as tk
from tkinter import ttk, messagebox
from core.timer import PomodoroTimer
from core.storage import save_tomato, get_today_count
from ui.app_window import AppWindow
from ui.widgets import RoundedCard, TimeAdjuster
from ui.styles import (
    BG_COLOR, SETTING_BG, BTN_START_BG, BTN_RESET_BG, TEXT_LIGHT, TEXT_DARK,
    WORK_COLOR, BREAK_COLOR
)

class PomodoroApp:
    def __init__(self):
        self.window = AppWindow()
        self.timer = PomodoroTimer()

        # 调节变量
        self.work_var = tk.IntVar(value=self.timer.work_min)
        self.short_var = tk.IntVar(value=self.timer.short_break)
        self.long_var = tk.IntVar(value=self.timer.long_break)

        self._build_ui()
        self._update_counter_label()

    def _build_ui(self):
        # 时间调节区
        setting_frame = tk.Frame(self.window, bg=SETTING_BG, highlightbackground="#ddd", highlightthickness=1)
        setting_frame.pack(pady=(12, 0), padx=30, fill="x")

        self.work_adj = TimeAdjuster(setting_frame, "🔴 工作 (分)", self.work_var, "work", self._on_adjust_time)
        self.work_adj.pack(side="left", expand=True, pady=5)
        self.short_adj = TimeAdjuster(setting_frame, "🟢 短休息", self.short_var, "short", self._on_adjust_time)
        self.short_adj.pack(side="left", expand=True, pady=5)
        self.long_adj = TimeAdjuster(setting_frame, "🔵 长休息", self.long_var, "long", self._on_adjust_time)
        self.long_adj.pack(side="left", expand=True, pady=5)

        # 圆角计时卡片
        self.card = RoundedCard(self.window, width=400, height=180)
        self.card.pack(pady=20, padx=30, fill="both")
        self.card.set_text("25:00", WORK_COLOR)

        # 按钮区域
        btn_frame = tk.Frame(self.window, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Start.TButton", background=BTN_START_BG, foreground=TEXT_DARK,
                        borderwidth=0, focusthickness=0, font=("Helvetica", 13, "bold"), padding=(24, 10))
        style.map("Start.TButton", background=[("active", "#f4a261"), ("pressed", "#e76f51")])
        style.configure("Reset.TButton", background=BTN_RESET_BG, foreground="white",
                        borderwidth=0, focusthickness=0, font=("Helvetica", 13, "bold"), padding=(24, 10))
        style.map("Reset.TButton", background=[("active", "#e76f51"), ("pressed", "#d62828")])

        self.start_btn = ttk.Button(btn_frame, text="▶ 开始工作", style="Start.TButton", command=self._start_pause)
        self.start_btn.grid(row=0, column=0, padx=12)
        self.reset_btn = ttk.Button(btn_frame, text="↺ 重置", style="Reset.TButton", command=self._reset)
        self.reset_btn.grid(row=0, column=1, padx=12)

        # 统计区
        counter_frame = tk.Frame(self.window, bg=BG_COLOR)
        counter_frame.pack(pady=18)
        self.counter_label = tk.Label(counter_frame, text="", font=("Helvetica", 12), fg=TEXT_LIGHT, bg=BG_COLOR)
        self.counter_label.pack()

        tip = tk.Label(self.window, text="拖动顶部移动窗口  ·  点击 ✕ 关闭", font=("Helvetica", 9), fg=TEXT_LIGHT, bg=BG_COLOR)
        tip.pack(side="bottom", pady=10)

    def _on_adjust_time(self, time_type, value):
        if self.timer.running:
            messagebox.showwarning("提示", "请先暂停或重置计时再调整时间")
            return
        # 更新核心时长
        if time_type == "work":
            self.timer.work_min = value
        elif time_type == "short":
            self.timer.short_break = value
        else:
            self.timer.long_break = value
        self.timer.reset()
        self.card.set_text("25:00" if time_type != "work" else f"{value:02d}:00", WORK_COLOR)
        self._update_button_text()

    def _start_pause(self):
        self.timer.start_pause(self.window, self._on_update, self._on_finish)
        self._update_button_text()

    def _reset(self):
        self.timer.reset()
        self.card.set_text(f"{self.timer.work_min:02d}:00", WORK_COLOR)
        self._update_button_text()

    def _on_update(self, text, color):
        self.card.set_text(text, color)

    def _on_finish(self, event_type):
        if event_type == "work_done":
            save_tomato()
            self._update_counter_label()
            messagebox.showinfo("🍅 完成", "一个番茄时间结束，休息一下吧！")
            # 自动进入休息
            if self.timer.tomato_count % 4 == 0:
                self.timer.is_break = True
                self.timer.remaining = self.timer.long_break * 60
            else:
                self.timer.is_break = True
                self.timer.remaining = self.timer.short_break * 60
            self.timer.running = False
            self.card.set_text(f"{self.timer.remaining // 60:02d}:00", BREAK_COLOR)
        else:  # break_done
            messagebox.showinfo("☕ 休息结束", "休息结束，开始新的番茄！")
            self.timer.is_break = False
            self.timer.remaining = self.timer.work_min * 60
            self.timer.running = False
            self.card.set_text(f"{self.timer.work_min:02d}:00", WORK_COLOR)
        self._update_button_text()

    def _update_button_text(self):
        if self.timer.running:
            self.start_btn.config(text="⏸ 暂停")
        else:
            if self.timer.is_break:
                self.start_btn.config(text="☕ 开始休息")
            else:
                self.start_btn.config(text="▶ 开始工作")

    def _update_counter_label(self):
        count = get_today_count()
        self.counter_label.config(text=f"今日番茄 🍅 × {count}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PomodoroApp()
    app.run()