import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.fileio.exporter import ExcelExporter, CSVExporter


class ClientController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        # Options frame
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.job_label = ttk.Label(options_frame, text="", font=("Helvetica", 18, "bold"))
        self.job_label.pack(pady=(0, 30))

        self.linkedin_conversation_btn = ttk.Button(options_frame, text="LinkedIn Conversation", command=self.open_linkedin_conversation_popup, width=20)
        self.linkedin_conversation_btn.pack(pady=10)

        self.email_conversation_btn = ttk.Button(options_frame, text="Email Conversation", command=self.open_email_conversation_popup, width=20)
        self.email_conversation_btn.pack(pady=10)

        self.export_btn = ttk.Button(options_frame, text="Export", command=self.open_export_popup, width=20)
        self.export_btn.pack(pady=10)

        self.exit_btn = ttk.Button(options_frame, text="Back to job menu", command=self.go_to_job, width=20)
        self.exit_btn.pack(pady=(30, 10))

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # self.update_client()

    def hide(self):
        self.frame.pack_forget()

    def update_client(self):
        self.job_label.config(text=self.app.selected_client.name)

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

        ttk.Button(button_frame, text="Back", command=popup.destroy).pack()

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

    def open_export_popup(self):
        client_name = self.app.selected_client.get_name()

        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Button(frame, text="Export Client (XLS)", command=export_xls, width=20).pack(pady=10)
            ttk.Button(frame, text="Export Client (CSV)", command=export_csv, width=20).pack(pady=10)

        def export_xls():
            exporter = ExcelExporter()
            exporter.export_specific_client(self.app.selected_job.get_name(), self.app.selected_client.get_name())
            messagebox.showinfo("Export", f"Success, f'{client_name} exported successfully!")

        def export_csv():
            exporter = CSVExporter()
            exporter.export_specific_client(self.app.selected_job.get_name(), self.app.selected_client.get_name())
            messagebox.showinfo("Export", f"Success, f'{client_name} exported successfully!")

        self.open_popup("Export", content)

    def go_to_job(self):
        self.app.show_frame('job')
