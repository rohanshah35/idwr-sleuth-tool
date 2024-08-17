# Handles loading screen within GUI

import tkinter as tk
import ttkbootstrap as ttk


class LoadingScreenController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)
        self.label = ttk.Label(self.frame, text="LOADING...", font=("Helvetica", 16, "bold"))
        self.label.pack(expand=True)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()