import tkinter as tk
from tkinter import ttk
import sv_ttk
from ui.styles import BG_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, CARD_COLOR, ACCENT
from core.storage import load_data

class HistoryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("历史记录")
        self.configure(bg=BG_COLOR)
        self.geometry("320x360")
        self.resizable(False, False)
        sv_ttk.set_theme("light")
        self._center(parent)

        # 标题
        title_frame = tk.Frame(self, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=(16, 8))
        tk.Label(title_frame, text="📊 每日番茄统计",
                 font=("Segoe UI", 14, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_COLOR).pack()

        # 列表区域（白色卡片）
        list_container = tk.Frame(self, bg=CARD_COLOR,
                                  highlightbackground="#e0e0e0", highlightthickness=1)
        list_container.pack(padx=20, pady=8, fill="both", expand=True)
        list_container.pack_propagate(False)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_container,
            font=("Segoe UI", 11),
            bg=CARD_COLOR, fg=TEXT_PRIMARY,
            selectbackground=ACCENT,
            selectforeground="white",
            yscrollcommand=scrollbar.set,
            relief="flat",
            highlightthickness=0,
            bd=0,
        )
        self.listbox.pack(fill="both", expand=True, padx=8, pady=8)
        scrollbar.config(command=self.listbox.yview)

        self._load_data()

        # 关闭按钮
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=(4, 16))
        ttk.Button(btn_frame, text="关闭",
                   style="Secondary.TButton",
                   command=self.destroy).pack()

    def _load_data(self):
        data = load_data()
        if not data:
            self.listbox.insert("end", "暂无记录")
        else:
            for date, count in sorted(data.items(), reverse=True):
                self.listbox.insert("end", f"  {date}     🍅 × {count}")

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        w = 320
        h = 360
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")