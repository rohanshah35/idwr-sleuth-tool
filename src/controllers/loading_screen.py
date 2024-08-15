import tkinter as tk
import ttkbootstrap as ttk


class LoadingScreenController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)
        self.label = ttk.Label(self.frame, text="LOADING...", font=("Helvetica", 16, "bold"))
        self.label.pack(expand=True)

        # self.progress = ttk.Progressbar(self.frame, mode="indeterminate", length=300)
        # self.progress.pack(pady=10)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # self.progress.start()

    def hide(self):
        # self.progress.stop()
        self.frame.pack_forget()