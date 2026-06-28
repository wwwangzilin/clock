import tkinter as tk
from tkinter import ttk
import ctypes
import sv_ttk
from core.timer import PomodoroTimer
from core.storage import save_tomato, get_today_count
from ui.app_window import AppWindow
from ui.widgets import TimerCard, TimeAdjuster
from ui.styles import (
    BG_COLOR, ACCENT,
    TEXT_PRIMARY, TEXT_SECONDARY, BREAK_COLOR, CARD_COLOR
)
from ui.settings_window import SettingsWindow
from ui.history_window import HistoryWindow
from ui.animations import fade_update_time

# ── Windows 高 DPI 感知（必须在创建任何窗口前调用）──
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)      # Per-Monitor V2
except Exception:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per-Monitor
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()   # System DPI
        except Exception:
            pass

class PomodoroApp:
    def __init__(self):
        self.window = AppWindow()
        self.timer = PomodoroTimer()

        self.work_var = tk.IntVar(value=self.timer.work_min)
        self.short_var = tk.IntVar(value=self.timer.short_break)
        self.long_var = tk.IntVar(value=self.timer.long_break)

        # 应用 sv-ttk 主题（Windows 11 风格）
        sv_ttk.set_theme("light")

        # 配置自定义 ttk 样式
        self._setup_styles()

        self._build_ui()
        self._build_menu()
        self._update_counter_label()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("Primary.TButton",
                        font=("Segoe UI", 12, "bold"),
                        padding=(32, 10))
        style.configure("Secondary.TButton",
                        font=("Segoe UI", 12),
                        padding=(32, 10))

    # ---------- 菜单 ----------
    def _build_menu(self):
        menubar = tk.Menu(self.window, font=("Segoe UI", 10), bg=CARD_COLOR, fg=TEXT_PRIMARY)
        self.window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10), bg=CARD_COLOR, fg=TEXT_PRIMARY)
        file_menu.add_command(label="⚙ 系统设置", command=self._open_settings)
        file_menu.add_command(label="📊 历史记录", command=self._open_history)
        file_menu.add_separator()
        file_menu.add_command(label="✕ 退出", command=self.window.destroy)
        menubar.add_cascade(label="🍅 番茄钟", menu=file_menu)

    def _open_settings(self):
        SettingsWindow(self.window, self.timer, self._on_settings_applied)

    def _on_settings_applied(self):
        self.work_var.set(self.timer.work_min)
        self.short_var.set(self.timer.short_break)
        self.long_var.set(self.timer.long_break)
        self._reset()

    def _open_history(self):
        HistoryWindow(self.window)

    # ---------- UI 构建 ----------
    def _build_ui(self):
        # 主容器
        main = tk.Frame(self.window, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=32, pady=(16, 24))

        # ── 时间调节区 ──
        setting_frame = tk.Frame(main, bg=CARD_COLOR,
                                 highlightbackground="#e0e0e0", highlightthickness=1)
        setting_frame.pack(pady=(0, 20), fill="x", ipady=4)

        self.work_adj = TimeAdjuster(setting_frame, "工作 (分)", self.work_var, "work", self._on_adjust_time)
        self.work_adj.pack(side="left", expand=True, pady=6)
        self.short_adj = TimeAdjuster(setting_frame, "短休息", self.short_var, "short", self._on_adjust_time)
        self.short_adj.pack(side="left", expand=True, pady=6)
        self.long_adj = TimeAdjuster(setting_frame, "长休息", self.long_var, "long", self._on_adjust_time)
        self.long_adj.pack(side="left", expand=True, pady=6)

        # ── 计时卡片 ──
        self.card = TimerCard(main)
        self.card.pack(fill="both", expand=True)
        self.card.set_time("25:00", ACCENT)

        # 渐入渐出动画状态追踪
        self._fade_cancel = None

        # ── 按钮区域 ──
        btn_frame = tk.Frame(main, bg=BG_COLOR)
        btn_frame.pack(pady=(20, 0))

        self.start_btn = ttk.Button(
            btn_frame, text="▶ 开始专注",
            style="Primary.TButton",
            command=self._start_pause
        )
        self.start_btn.pack(side="left", padx=6)

        self.reset_btn = ttk.Button(
            btn_frame, text="↻ 重置",
            style="Secondary.TButton",
            command=self._reset
        )
        self.reset_btn.pack(side="left", padx=6)

        # ── 统计区 ──
        counter_frame = tk.Frame(main, bg=BG_COLOR)
        counter_frame.pack(pady=(16, 0))
        self.counter_label = tk.Label(
            counter_frame, text="",
            font=("Segoe UI", 11), fg=TEXT_SECONDARY, bg=BG_COLOR
        )
        self.counter_label.pack()

    # ---------- 交互逻辑 ----------
    def _on_adjust_time(self, time_type, value):
        if self.timer.running:
            return
        if time_type == "work":
            self.timer.work_min = value
        elif time_type == "short":
            self.timer.short_break = value
        else:
            self.timer.long_break = value
        self.timer.reset()
        new_text = f"{value:02d}:00"
        self.card.set_time(new_text, ACCENT)
        self._update_button_text()

    def _start_pause(self):
        self.timer.start_pause(self.window, self._on_update, self._on_finish)
        self._update_button_text()

    def _reset(self):
        self.timer.reset()
        self.card.set_time(f"{self.timer.work_min:02d}:00", ACCENT)
        self.card.set_status("点击下方按钮开始专注")
        self._update_button_text()

    def _on_update(self, text, color):
        # 取消上一次未完成的动画
        if self._fade_cancel:
            self._fade_cancel()
        # 使用 styles 定义色（忽略 timer.py 传来的硬编码色）
        actual_color = BREAK_COLOR if self.timer.is_break else ACCENT
        # 渐入渐出动画更新数字
        self._fade_cancel = fade_update_time(
            self.card.time_label, text, actual_color,
            bg_color=CARD_COLOR,
            fade_steps=12,
            fade_interval=16,
        )

    def _on_finish(self, event_type):
        if event_type == "work_done":
            save_tomato()
            self._update_counter_label()
            if self.timer.tomato_count % 4 == 0:
                self.timer.is_break = True
                self.timer.remaining = self.timer.long_break * 60
            else:
                self.timer.is_break = True
                self.timer.remaining = self.timer.short_break * 60
            self.timer.running = False
            new_color = BREAK_COLOR
            new_text = f"{self.timer.remaining // 60:02d}:00"
            self.card.set_status("☕ 休息时间，放松一下吧")
        else:
            self.timer.is_break = False
            self.timer.remaining = self.timer.work_min * 60
            self.timer.running = False
            new_color = ACCENT
            new_text = f"{self.timer.work_min:02d}:00"
            self.card.set_status("开始新的番茄时间！")

        # 取消上一次动画，用渐入渐出更新完成后的时间
        if self._fade_cancel:
            self._fade_cancel()
        self._fade_cancel = fade_update_time(
            self.card.time_label, new_text, new_color,
            bg_color=CARD_COLOR,
            fade_steps=15,
            fade_interval=16,
        )
        self._update_button_text()

    def _update_button_text(self):
        if self.timer.running:
            self.start_btn.config(text="⏸ 暂停")
            self.card.set_status("专注中...")
        else:
            if self.timer.is_break:
                self.start_btn.config(text="▶ 开始休息")
            else:
                self.start_btn.config(text="▶ 开始专注")

    def _update_counter_label(self):
        count = get_today_count()
        self.counter_label.config(text=f"今日完成 🍅 × {count}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PomodoroApp()
    app.run()