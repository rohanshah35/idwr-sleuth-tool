import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

from src.fileio.file_handler import JobHandler
from src.structures.job import Job


class ClientController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        # Options frame
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.job_label = ttk.Label(options_frame, text="", font=("Helvetica", 18, "bold"))
        self.job_label.pack(pady=(0, 30))

        # if self.app.selected_job:
        #     self.job_label = ttk.Label(options_frame, text=self.app.selected_job.getName(), font=("Helvetica", 18, "bold"))
        #     self.job_label.pack(pady=(0, 30))

        self.select_job_btn = ttk.Button(options_frame, text="Open LinkedIn Conversation", command=self.open_linkedin_conversation_popup, width=20)
        self.select_job_btn.pack(pady=10)

        self.create_job_btn = ttk.Button(options_frame, text="Open Email Conversation", command=self.open_email_conversation_popup, width=20)
        self.create_job_btn.pack(pady=10)

        self.exit_btn = ttk.Button(options_frame, text="Back to job menu", command=self.go_to_job, width=20)
        self.exit_btn.pack(pady=(30, 10))

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # self.update_client()

    def hide(self):
        self.frame.pack_forget()

    # def update_client(self):
    #     if self.app.selected_job:
    #         self.job_label.config(text=self.app.selected_job.name)

    def open_popup(self, title, content_func, width=800, height=600):
        popup = tk.Toplevel(self.app.root)
        popup.title(title)
        popup.geometry(f"{width}x{height}")
        popup.transient(self.app.root)
        popup.grab_set()

        self.center_popup(popup, width, height)

        content_frame = ttk.Frame(popup, padding="20 20 20 20")
        content_frame.pack(fill=tk.BOTH, expand=True)

        content_func(content_frame)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(side=BOTTOM, fill=X, pady=10)

        ttk.Button(button_frame, text="Back to client menu", command=popup.destroy).pack()

        return popup

    def center_popup(self, popup, width, height):
        self.app.root.update_idletasks()
        main_width = self.app.root.winfo_width()
        main_height = self.app.root.winfo_height()
        main_x = self.app.root.winfo_x()
        main_y = self.app.root.winfo_y()

        position_right = int(main_x + (main_width / 2) - (width / 2))
        position_down = int(main_y + (main_height / 2) - (height / 2))

        popup.geometry(f"{width}x{height}+{position_right}+{position_down}")

    def open_linkedin_conversation_popup(self):
        def content(frame):
            ttk.Label(frame, text="LinkedIn Conversation", font=("Helvetica", 16, "bold")).pack(pady=10)

        popup = self.open_popup("LinkedIn Conversation", content)

    def open_email_conversation_popup(self):
        def content(frame):
            ttk.Label(frame, text="Email Conversation", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

        popup = self.open_popup("Email Conversation", content)

    def go_to_job(self):
        self.app.show_frame('job')
