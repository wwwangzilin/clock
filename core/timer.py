from typing import Callable

class PomodoroTimer:
    """番茄钟核心逻辑，完全不依赖 GUI"""
    def __init__(self, work_min=25, short_break=5, long_break=15):
        self.work_min = work_min
        self.short_break = short_break
        self.long_break = long_break
        self.reset()

    def reset(self):
        self.remaining = self.work_min * 60
        self.running = False
        self.is_break = False
        self.tomato_count = 0
        self._after_id = None

    def _clear_after(self, root):
        if self._after_id:
            root.after_cancel(self._after_id)
            self._after_id = None

    def start_pause(self, root, on_update: Callable, on_finish: Callable):
        if self.remaining == 0:
            self.reset()
        self.running = not self.running
        if self.running:
            self._tick(root, on_update, on_finish)

    def _tick(self, root, on_update, on_finish):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            mins, secs = divmod(self.remaining, 60)
            color = "#e76f51" if not self.is_break else "#2a9d8f"
            on_update(f"{mins:02d}:{secs:02d}", color)
            self._after_id = root.after(1000, lambda: self._tick(root, on_update, on_finish))
        elif self.remaining == 0:
            self.running = False
            if not self.is_break:
                self.tomato_count += 1
                on_finish("work_done")
            else:
                on_finish("break_done")

    def adjust_times(self, work=None, short=None, long=None):
        if work is not None:
            self.work_min = work
        if short is not None:
            self.short_break = short
        if long is not None:
            self.long_break = long
        self.reset()

    def get_state(self):
        return {
            "remaining": self.remaining,
            "running": self.running,
            "is_break": self.is_break,
            "tomato_count": self.tomato_count,
            "work_min": self.work_min,
            "short_break": self.short_break,
            "long_break": self.long_break
        }