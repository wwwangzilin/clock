def _parse_hex(color):
    """将 #rrggbb 转为 (r, g, b) 整数元组"""
    return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)


def _lerp_color(c1, c2, t):
    """线性插值两个颜色，t 范围 0~1"""
    r1, g1, b1 = _parse_hex(c1) if isinstance(c1, str) else c1
    r2, g2, b2 = _parse_hex(c2) if isinstance(c2, str) else c2
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def fade_label_color(label, from_color, to_color, steps=20, interval=16, callback=None):
    """
    让 Label 的 foreground 颜色从 from_color 渐变到 to_color。
    返回一个取消函数，调用后可终止动画。
    """
    _keep_running = True
    after_ids = []

    def cancel():
        nonlocal _keep_running
        _keep_running = False
        for aid in after_ids:
            try:
                label.after_cancel(aid)
            except RuntimeError:
                pass
        after_ids.clear()

    def _step(i):
        if not _keep_running:
            return
        color = _lerp_color(from_color, to_color, i / steps)
        try:
            label.config(fg=color)
        except tk.TclError:
            return
        if i < steps:
            aid = label.after(interval, lambda: _step(i + 1))
            after_ids.append(aid)
        elif callback:
            callback()

    _step(0)
    return cancel


def fade_update_time(label, new_text, new_color, bg_color="#ffffff",
                     fade_steps=12, fade_interval=16, callback=None):
    """
    带渐入渐出效果更新 Label 的时间显示：
      渐出（当前颜色 → bg_color）→ 更新文字 → 渐入（bg_color → new_color）
    返回一个取消函数。
    """
    _keep_running = True

    def cancel():
        nonlocal _keep_running
        _keep_running = False

    current_color = label.cget("fg")

    # ── 第 2 阶段：渐入 ──
    def do_fade_in():
        if not _keep_running:
            return
        fade_label_color(label, bg_color, new_color, fade_steps, fade_interval, callback)

    # ── 第 1 阶段：更新文字 → 渐入 ──
    def do_update_text():
        if not _keep_running:
            return
        try:
            label.config(text=new_text)
        except tk.TclError:
            return
        do_fade_in()

    # ── 第 0 阶段：渐出 ──
    fade_label_color(label, current_color, bg_color, fade_steps, fade_interval, do_update_text)
    return cancel


import tkinter as tk