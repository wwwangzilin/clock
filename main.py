import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date

# ------------------ 常量 ------------------
WORK_MIN = 25          # 工作时长（分钟）
SHORT_BREAK = 5        # 短休息
LONG_BREAK = 15        # 长休息（每4个番茄后）
FONT_NAME = "Arial"
WORK_COLOR = "#e74c3c"     # 红色
BREAK_COLOR = "#2ecc71"    # 绿色

# ------------------ 全局状态 ------------------
timer_running = False
remaining = WORK_MIN * 60   # 秒
tomato_count = 0            # 当前周期完成的番茄数
is_break = False            # 是否处于休息阶段

# ------------------ 数据存储 ------------------
DATA_FILE = "tomato_data.json"

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
        canvas.itemconfig(timer_text, text=format_time(remaining))
        root.after(1000, update_timer)
    elif remaining == 0:
        timer_running = False
        if not is_break:
            # 一个番茄完成
            tomato_count += 1
            save_tomato()
            update_counter_label()
            messagebox.showinfo("番茄钟", "一个番茄时间结束，休息一下吧！")
            # 判断长休息还是短休息
            if tomato_count % 4 == 0:
                set_break(LONG_BREAK)
            else:
                set_break(SHORT_BREAK)
        else:
            # 休息结束
            messagebox.showinfo("番茄钟", "休息结束，开始新的番茄！")
            set_work()

def start_pause():
    global timer_running
    if remaining == 0:
        # 重置后再开始
        reset_timer()
    timer_running = not timer_running
    if timer_running:
        update_timer()
    update_button_text()

def reset_timer():
    global timer_running, remaining, is_break
    timer_running = False
    is_break = False
    remaining = WORK_MIN * 60
    canvas.itemconfig(timer_text, text=format_time(remaining), fill=WORK_COLOR)
    update_button_text()

def set_work():
    global is_break, remaining, timer_running
    is_break = False
    remaining = WORK_MIN * 60
    timer_running = False
    canvas.itemconfig(timer_text, text=format_time(remaining), fill=WORK_COLOR)
    update_button_text()

def set_break(minutes):
    global is_break, remaining, timer_running
    is_break = True
    remaining = minutes * 60
    timer_running = False
    canvas.itemconfig(timer_text, text=format_time(remaining), fill=BREAK_COLOR)
    update_button_text()

def update_button_text():
    if timer_running:
        start_btn.config(text="暂停")
    else:
        if is_break:
            start_btn.config(text="开始休息")
        else:
            start_btn.config(text="开始工作")

def update_counter_label():
    today = date.today().isoformat()
    data = load_data()
    count = data.get(today, 0)
    counter_label.config(text=f"今日番茄：{count}")

# ------------------ 界面搭建 ------------------
root = tk.Tk()
root.title("番茄工作法")
root.geometry("350x320")
root.resizable(False, False)

# 计时显示（用Canvas以便换颜色）
canvas = tk.Canvas(root, width=200, height=200, highlightthickness=0)
canvas.pack(pady=20)
timer_text = canvas.create_text(100, 100, text="25:00", fill=WORK_COLOR,
                                font=(FONT_NAME, 48, "bold"))

# 按钮区
btn_frame = tk.Frame(root)
btn_frame.pack()

start_btn = tk.Button(btn_frame, text="开始工作", command=start_pause, width=10, font=(FONT_NAME, 12))
start_btn.grid(row=0, column=0, padx=5)

reset_btn = tk.Button(btn_frame, text="重置", command=reset_timer, width=10, font=(FONT_NAME, 12))
reset_btn.grid(row=0, column=1, padx=5)

# 今日统计
counter_label = tk.Label(root, text="今日番茄：0", font=(FONT_NAME, 12))
counter_label.pack(pady=15)
update_counter_label()

# 退出时保存（已经及时保存了，这里可以省略）
root.mainloop()