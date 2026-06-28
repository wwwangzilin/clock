import tkinter as tk
from ui.styles import BG_COLOR, TEXT_DARK, TEXT_LIGHT
from core.storage import load_data

class HistoryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("历史记录")
        self.configure(bg=BG_COLOR)
        self.geometry("280x300")
        self.resizable(False, False)
        self._center(parent)

        tk.Label(self, text="每日番茄统计", font=("Helvetica", 14, "bold"),
                 fg=TEXT_DARK, bg=BG_COLOR).pack(pady=10)

        # 列表区域
        list_frame = tk.Frame(self, bg=BG_COLOR)
        list_frame.pack(padx=20, pady=5, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(list_frame, font=("Helvetica", 11),
                                  bg="white", fg=TEXT_DARK, selectbackground="#e9dbbd",
                                  yscrollcommand=scrollbar.set)
        self.listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        self._load_data()

        tk.Button(self, text="关闭", font=("Helvetica", 11),
                  bg="#f4a261", fg="white", relief="flat",
                  command=self.destroy).pack(pady=10)

    def _load_data(self):
        data = load_data()
        if not data:
            self.listbox.insert("end", "暂无记录")
        else:
            for date, count in sorted(data.items(), reverse=True):
                self.listbox.insert("end", f"{date}  🍅 × {count}")

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        w = 280
        h = 300
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")