def animate_color(canvas, item_id, from_color, to_color, steps=10, interval=20):
    """数字颜色渐变（预留，未来可调用）"""
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