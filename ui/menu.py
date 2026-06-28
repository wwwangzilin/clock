import tkinter as tk
from ui.styles import BG_COLOR, TEXT_DARK, TEXT_LIGHT, CARD_COLOR

class PopupMenu(tk.Toplevel):
    def __init__(self, parent, items):
        """
        items: [(text, command), ...]
        """
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg=CARD_COLOR, highlightbackground="#ccc", highlightthickness=1)

        for text, cmd in items:
            btn = tk.Button(
                self, text=text, font=("Helvetica", 11),
                fg=TEXT_DARK, bg=CARD_COLOR, activebackground="#e9dbbd",
                relief="flat", padx=20, pady=8, anchor="w", width=12,
                command=lambda c=cmd: (c(), self.destroy())
            )
            btn.pack(fill="x")

        # 放在父窗口标题栏下方
        self.update_idletasks()
        x = parent.winfo_x() + 20
        y = parent.winfo_y() + 40
        self.geometry(f"+{x}+{y}")
        self.focus_set()
        self.bind("<FocusOut>", lambda e: self.destroy())

    def _close(self):
        self.destroy()