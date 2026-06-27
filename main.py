import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date

# ========== 启用高 DPI 支持 ==========
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass
# =====================================

# ------------------ 初始可调时长 ------------------
WORK_MIN = 25
SHORT_BREAK = 5
LONG_BREAK = 15

# ------------------ 配色 ------------------
BG_COLOR = "#faf3e0"
TITLE_BG = "#e9dbbd"
CARD_COLOR = "#ffffff"
WORK_COLOR = "#e76f51"
BREAK_COLOR = "#2a9d8f"
TEXT_DARK = "#264653"
TEXT_LIGHT = "#6c757d"
BTN_START_BG = "#e9c46a"
BTN_RESET_BG = "#f4a261"
SETTING_BG = "#f0e6d2"

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
        canvas.itemconfig(timer_text_id, text=format_time(remaining))
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
    update_timer_color(WORK_COLOR)
    canvas.itemconfig(timer_text_id, text=format_time(remaining))
    update_button_state()

def set_work():
    global is_break, remaining, timer_running
    is_break = False
    remaining = WORK_MIN * 60
    timer_running = False
    update_timer_color(WORK_COLOR)
    canvas.itemconfig(timer_text_id, text=format_time(remaining))
    update_button_state()

def set_break(minutes):
    global is_break, remaining, timer_running
    is_break = True
    remaining = minutes * 60
    timer_running = False
    update_timer_color(BREAK_COLOR)
    canvas.itemconfig(timer_text_id, text=format_time(remaining))
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

# 修改计时数字颜色
def update_timer_color(color):
    canvas.itemconfig(timer_text_id, fill=color)

# ------------------ 时间调节功能 ------------------
def adjust_time(var, delta, time_type):
    new_val = var.get() + delta
    if new_val < 1:
        new_val = 1
    elif new_val > 120:
        new_val = 120

    if timer_running:
        messagebox.showwarning("提示", "请先暂停或重置计时再调整时间")
        return

    var.set(new_val)
    global WORK_MIN, SHORT_BREAK, LONG_BREAK
    if time_type == "work":
        WORK_MIN = new_val
    elif time_type == "short":
        SHORT_BREAK = new_val
    else:
        LONG_BREAK = new_val

    reset_timer()

# ------------------ 无边框拖动功能 ------------------
def start_move(event):
    root.x = event.x
    root.y = event.y

def on_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

# ------------------ 绘制圆角矩形辅助函数 ------------------
def draw_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """在canvas上绘制一个圆角矩形，返回四个部分的ID组成的元组"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# ------------------ 界面搭建 ------------------
root = tk.Tk()
root.overrideredirect(True)

window_width = 460
window_height = 540
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2) - 30
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg=BG_COLOR)

# ---- 自定义标题栏（圆角） ----
title_bar = tk.Canvas(root, bg=BG_COLOR, height=40, highlightthickness=0)
title_bar.pack(fill="x")
# 绘制标题栏圆角矩形背景
draw_rounded_rect(title_bar, 4, 4, window_width - 4, 36, radius=18, fill=TITLE_BG, outline="")
# 标题文字
title_bar.create_text(20, 20, anchor="w", text="🍅 番茄钟",
                      font=("Helvetica", 12, "bold"), fill=TEXT_DARK)
# 关闭按钮（用Canvas模拟）
close_btn_id = title_bar.create_text(window_width - 20, 20, anchor="e", text="✕",
                                     font=("Helvetica", 14), fill=TEXT_DARK)
# 关闭按钮悬停变色
def on_close_enter(event):
    title_bar.itemconfig(close_btn_id, fill="red")
def on_close_leave(event):
    title_bar.itemconfig(close_btn_id, fill=TEXT_DARK)
title_bar.tag_bind(close_btn_id, "<Enter>", on_close_enter)
title_bar.tag_bind(close_btn_id, "<Leave>", on_close_leave)
title_bar.tag_bind(close_btn_id, "<Button-1>", lambda e: root.destroy())

# 拖动绑定（整个标题栏区域）
title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", on_move)

# ---- 时间调节区 ----
setting_frame = tk.Frame(root, bg=SETTING_BG, highlightbackground="#ddd", highlightthickness=1)
setting_frame.pack(pady=(12, 0), padx=30, fill="x")

work_var = tk.IntVar(value=WORK_MIN)
short_var = tk.IntVar(value=SHORT_BREAK)
long_var = tk.IntVar(value=LONG_BREAK)

def make_adjuster(parent, label_text, var, time_type):
    frame = tk.Frame(parent, bg=SETTING_BG)
    frame.pack(side="left", expand=True, pady=5)

    lbl = tk.Label(frame, text=label_text, font=("Helvetica", 9), fg=TEXT_LIGHT, bg=SETTING_BG)
    lbl.pack()

    inner = tk.Frame(frame, bg=SETTING_BG)
    inner.pack()

    btn_minus = tk.Button(
        inner, text="−", font=("Helvetica", 10, "bold"),
        width=2, relief="flat", bg="#e0d5c1", activebackground="#d4c9b5",
        command=lambda: adjust_time(var, -1, time_type)
    )
    btn_minus.pack(side="left")

    val_label = tk.Label(
        inner, textvariable=var, font=("Helvetica", 12, "bold"),
        fg=TEXT_DARK, bg=SETTING_BG, width=3
    )
    val_label.pack(side="left")

    btn_plus = tk.Button(
        inner, text="+", font=("Helvetica", 10, "bold"),
        width=2, relief="flat", bg="#e0d5c1", activebackground="#d4c9b5",
        command=lambda: adjust_time(var, 1, time_type)
    )
    btn_plus.pack(side="left")

    return frame

work_adj = make_adjuster(setting_frame, "🔴 工作 (分)", work_var, "work")
short_adj = make_adjuster(setting_frame, "🟢 短休息", short_var, "short")
long_adj = make_adjuster(setting_frame, "🔵 长休息", long_var, "long")

# ---- 圆角计时卡片 ----
card_canvas = tk.Canvas(root, bg=BG_COLOR, height=180, highlightthickness=0)
card_canvas.pack(pady=20, padx=30, fill="both")

# 绘制圆角矩形背景
card_radius = 30
card_x1, card_y1 = 0, 0
card_x2, card_y2 = card_canvas.winfo_reqwidth(), 180  # 后面会更新宽度
# 先绘制占位，等canvas尺寸确定后再更新
def draw_card_bg():
    w = card_canvas.winfo_width()
    h = card_canvas.winfo_height()
    card_canvas.delete("card_bg")
    draw_rounded_rect(card_canvas, 4, 4, w-4, h-4, radius=card_radius,
                      fill=CARD_COLOR, outline="#e0e0e0", tags="card_bg")
    # 保证文字在最上层
    card_canvas.tag_raise(timer_text_id)

timer_text_id = card_canvas.create_text(
    card_canvas.winfo_reqwidth()//2, 90,
    text=format_time(remaining),
    font=("Helvetica", 58, "bold"),
    fill=WORK_COLOR
)

# 绑定尺寸变化事件
def on_card_resize(event):
    draw_card_bg()
    # 更新文字位置居中
    card_canvas.coords(timer_text_id, event.width//2, event.height//2)

card_canvas.bind("<Configure>", on_card_resize)

# ---- 按钮区域 ----
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
    font=("Helvetica", 13, "bold"),
    padding=(24, 10)
)
style.map("Start.TButton",
          background=[("active", "#f4a261"), ("pressed", "#e76f51")])
style.configure(
    "Reset.TButton",
    background=BTN_RESET_BG,
    foreground="white",
    borderwidth=0,
    focusthickness=0,
    font=("Helvetica", 13, "bold"),
    padding=(24, 10)
)
style.map("Reset.TButton",
          background=[("active", "#e76f51"), ("pressed", "#d62828")])

start_btn = ttk.Button(btn_frame, text="▶ 开始工作", style="Start.TButton", command=start_pause)
start_btn.grid(row=0, column=0, padx=12)

reset_btn = ttk.Button(btn_frame, text="↺ 重置", style="Reset.TButton", command=reset_timer)
reset_btn.grid(row=0, column=1, padx=12)

# ---- 底部统计 ----
counter_frame = tk.Frame(root, bg=BG_COLOR)
counter_frame.pack(pady=18)
counter_label = tk.Label(
    counter_frame,
    text="今日番茄 🍅 × 0",
    font=("Helvetica", 12),
    fg=TEXT_LIGHT,
    bg=BG_COLOR
)
counter_label.pack()
update_counter_label()

tip_label = tk.Label(
    root,
    text="拖动顶部移动窗口  ·  点击 ✕ 关闭",
    font=("Helvetica", 9),
    fg=TEXT_LIGHT,
    bg=BG_COLOR
)
tip_label.pack(side="bottom", pady=10)

root.mainloop()