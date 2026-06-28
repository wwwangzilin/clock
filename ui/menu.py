import tkinter as tk
from ui.styles import TEXT_PRIMARY, CARD_COLOR

class PopupMenu(tk.Toplevel):
    """弹出菜单（当前未使用，改用系统菜单栏）"""
    def __init__(self, parent, items):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg=CARD_COLOR, highlightbackground="#ccc", highlightthickness=1)

        for text, cmd in items:
            btn = tk.Button(
                self, text=text, font=("Segoe UI", 11),
                fg=TEXT_PRIMARY, bg=CARD_COLOR, activebackground="#e0e0e0",
                relief="flat", padx=20, pady=8, anchor="w", width=12,
                command=lambda c=cmd: (c(), self.destroy())
            )
            btn.pack(fill="x")

        self.update_idletasks()
        x = parent.winfo_x() + 20
        y = parent.winfo_y() + 40
        self.geometry(f"+{x}+{y}")
        self.focus_set()
        self.bind("<FocusOut>", lambda e: self.destroy())