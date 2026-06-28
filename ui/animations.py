def animate_color(canvas, item_id, from_color, to_color, steps=10, interval=20):
    """数字颜色渐变"""
    def _step(i):
        r1, g1, b1 = int(from_color[1:3], 16), int(from_color[3:5], 16), int(from_color[5:7], 16)
        r2, g2, b2 = int(to_color[1:3], 16), int(to_color[3:5], 16), int(to_color[5:7], 16)
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.itemconfig(item_id, fill=color)
        if i < steps:
            canvas.after(interval, lambda: _step(i + 1))
    _step(0)

def pulse_text(canvas, item_id, original_font, scale_min=0.9, duration=120, steps=6):
    """
    文字缩放脉冲：缩小再放大回原始大小
    original_font: 元组 ("Helvetica", 58, "bold")
    """
    orig_size = original_font[1]
    step_time = duration // steps // 2  # 一半缩小一半放大
    def _shrink(i):
        size = orig_size - (orig_size * (1 - scale_min)) * (i / steps)
        font = (original_font[0], int(size), original_font[2])
        canvas.itemconfig(item_id, font=font)
        if i < steps:
            canvas.after(step_time, lambda: _shrink(i + 1))
        else:
            _grow(0)
    def _grow(i):
        size = orig_size * scale_min + (orig_size * (1 - scale_min)) * (i / steps)
        font = (original_font[0], int(size), original_font[2])
        canvas.itemconfig(item_id, font=font)
        if i < steps:
            canvas.after(step_time, lambda: _grow(i + 1))
        else:
            # 恢复精确原始字体
            canvas.itemconfig(item_id, font=original_font)
    _shrink(0)