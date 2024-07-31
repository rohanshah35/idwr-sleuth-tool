import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class HomeController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        # Add your home page widgets here
        ttk.Label(self.frame, text="Home Page").pack(pady=20)
        ttk.Button(self.frame, text="Go to Jobs", command=lambda: app.show_frame('job')).pack()
        ttk.Button(self.frame, text="Go to Clients", command=lambda: app.show_frame('client')).pack()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()
