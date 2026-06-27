import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date

# ========== 关键：启用高 DPI 支持 ==========
import ctypes
try:
    # Windows 8.1 及以上
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        # Windows Vista/7
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass
# ===========================================

# ------------------ 常量 ------------------
WORK_MIN = 25
SHORT_BREAK = 5
LONG_BREAK = 15

# 配色方案
BG_COLOR = "#faf3e0"
CARD_COLOR = "#ffffff"
WORK_COLOR = "#e76f51"
BREAK_COLOR = "#2a9d8f"
TEXT_DARK = "#264653"
TEXT_LIGHT = "#6c757d"
BTN_START_BG = "#e9c46a"
BTN_RESET_BG = "#f4a261"

# ------------------ 全局状态 ------------------
timer_running = False
remaining = WORK_MIN * 60
tomato_count = 0
is_break = False

DATA_FILE = "tomato_data.json"

# ------------------ 数据存储 ------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tomato():
    today = date.today().isoformat()
    data = load_data()
    data[today] = data.get(today, 0) + 1
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ------------------ 计时逻辑 ------------------
def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def update_timer():
    global remaining, timer_running, is_break, tomato_count
    if timer_running and remaining > 0:
        remaining -= 1
        timer_label.config(text=format_time(remaining))
        root.after(1000, update_timer)
    elif remaining == 0:
        timer_running = False
        if not is_break:
            tomato_count += 1
            save_tomato()
            update_counter_label()
            messagebox.showinfo("🍅 完成", "一个番茄时间结束，休息一下吧！")
            if tomato_count % 4 == 0:
                set_break(LONG_BREAK)
            else:
                set_break(SHORT_BREAK)
        else:
            messagebox.showinfo("☕ 休息结束", "休息结束，开始新的番茄！")
            set_work()

def start_pause():
    global timer_running
    if remaining == 0:
        reset_timer()
    timer_running = not timer_running
    if timer_running:
        update_timer()
    update_button_state()

def reset_timer():
    global timer_running, remaining, is_break
    timer_running = False
    is_break = False
    remaining = WORK_MIN * 60
    timer_label.config(text=format_time(remaining), fg=WORK_COLOR)
    update_button_state()

def set_work():
    global is_break, remaining, timer_running
    is_break = False
    remaining = WORK_MIN * 60
    timer_running = False
    timer_label.config(text=format_time(remaining), fg=WORK_COLOR)
    update_button_state()

def set_break(minutes):
    global is_break, remaining, timer_running
    is_break = True
    remaining = minutes * 60
    timer_running = False
    timer_label.config(text=format_time(remaining), fg=BREAK_COLOR)
    update_button_state()

def update_button_state():
    if timer_running:
        start_btn.config(text="⏸ 暂停")
    else:
        if is_break:
            start_btn.config(text="☕ 开始休息")
        else:
            start_btn.config(text="▶ 开始工作")

def update_counter_label():
    today = date.today().isoformat()
    data = load_data()
    count = data.get(today, 0)
    counter_label.config(text=f"今日番茄 🍅 × {count}")

# ------------------ 界面搭建 ------------------
root = tk.Tk()
root.title("🍅 番茄钟")
root.geometry("380x420")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# 顶部标题栏
title_frame = tk.Frame(root, bg=BG_COLOR)
title_frame.pack(pady=(20, 5))
title_label = tk.Label(
    title_frame,
    text="🍅 Pomodoro Timer",
    font=("Helvetica", 18, "bold"),
    fg=TEXT_DARK,
    bg=BG_COLOR
)
title_label.pack()

# 计时卡片
card_frame = tk.Frame(root, bg=CARD_COLOR, highlightbackground="#e0e0e0", highlightthickness=1)
card_frame.pack(pady=20, padx=30, fill="both")
timer_label = tk.Label(
    card_frame,
    text="25:00",
    font=("Helvetica", 56, "bold"),
    fg=WORK_COLOR,
    bg=CARD_COLOR
)
timer_label.pack(pady=30)

# 按钮区域
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Start.TButton",
    background=BTN_START_BG,
    foreground=TEXT_DARK,
    borderwidth=0,
    focusthickness=0,
    font=("Helvetica", 12, "bold"),
    padding=(20, 10)
)
style.map("Start.TButton",
          background=[("active", "#f4a261"), ("pressed", "#e76f51")])
style.configure(
    "Reset.TButton",
    background=BTN_RESET_BG,
    foreground="white",
    borderwidth=0,
    focusthickness=0,
    font=("Helvetica", 12, "bold"),
    padding=(20, 10)
)
style.map("Reset.TButton",
          background=[("active", "#e76f51"), ("pressed", "#d62828")])

start_btn = ttk.Button(btn_frame, text="▶ 开始工作", style="Start.TButton", command=start_pause)
start_btn.grid(row=0, column=0, padx=10)

reset_btn = ttk.Button(btn_frame, text="↺ 重置", style="Reset.TButton", command=reset_timer)
reset_btn.grid(row=0, column=1, padx=10)

# 底部统计
counter_frame = tk.Frame(root, bg=BG_COLOR)
counter_frame.pack(pady=20)
counter_label = tk.Label(
    counter_frame,
    text="今日番茄 🍅 × 0",
    font=("Helvetica", 12),
    fg=TEXT_LIGHT,
    bg=BG_COLOR
)
counter_label.pack()
update_counter_label()

# 底部提示
tip_label = tk.Label(
    root,
    text="工作25分钟 · 休息5分钟 · 每4轮长休息15分钟",
    font=("Helvetica", 9),
    fg=TEXT_LIGHT,
    bg=BG_COLOR
)
tip_label.pack(side="bottom", pady=15)

root.mainloop()