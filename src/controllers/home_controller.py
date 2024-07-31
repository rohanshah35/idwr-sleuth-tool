import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

from src.fileio.file_handler import JobHandler


class HomeController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        self.app.user_manager.load_handlers()

        # Email display
        email_frame = ttk.Frame(self.frame)
        email_frame.pack(fill=X, pady=(0, 20))
        ttk.Label(email_frame, text="Email:", font=("Helvetica", 12)).pack(side=LEFT)
        self.email_label = ttk.Label(email_frame, text="Not set", font=("Helvetica", 12, "bold"))
        self.email_label.pack(side=LEFT, padx=(5, 0))

        # Options frame
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.select_job_btn = ttk.Button(options_frame, text="Select Job", command=self.open_select_job_popup, width=20)
        self.select_job_btn.pack(pady=10)

        self.create_job_btn = ttk.Button(options_frame, text="Create Job", command=self.open_create_job_popup, width=20)
        self.create_job_btn.pack(pady=10)

        self.delete_job_btn = ttk.Button(options_frame, text="Delete Job", command=self.open_delete_job_popup, width=20)
        self.delete_job_btn.pack(pady=10)

        self.export_btn = ttk.Button(options_frame, text="Export All Jobs", command=self.open_export_popup, width=20)
        self.export_btn.pack(pady=10)

        self.account_cred_btn = ttk.Button(options_frame, text="Settings", command=self.open_credentials_popup,
                                           width=20)
        self.account_cred_btn.pack(pady=(30, 10))

        self.exit_btn = ttk.Button(options_frame, text="Exit", command=self.exit_app, width=20)
        self.exit_btn.pack(pady=10)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_email()

    def hide(self):
        self.frame.pack_forget()

    def update_email(self):
        email = self.app.user_manager.user_data.get('linkedin_username', 'Not set')
        self.email_label.config(text=email if email else "Not set")

    def open_popup(self, title, content_func, width=600, height=400):
        popup = tk.Toplevel(self.app.root)
        popup.title(title)
        popup.geometry(f"{width}x{height}")
        popup.transient(self.app.root)
        popup.grab_set()

        # Center the popup on the main window
        self.center_popup(popup, width, height)

        content_frame = ttk.Frame(popup, padding="20 20 20 20")
        content_frame.pack(fill=tk.BOTH, expand=True)

        content_func(content_frame)

        ttk.Button(content_frame, text="Back to home menu", command=popup.destroy).pack(pady=(20, 0))

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

    def open_select_job_popup(self):
        def content(frame):
            ttk.Label(frame, text="Select Job", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
            # Add your select job widgets here

        self.open_popup("Select Job", content)

    def open_create_job_popup(self):
        def content(frame):
            ttk.Label(frame, text="Create Job", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
            # Add your create job widgets here

        self.open_popup("Create Job", content)

    def open_delete_job_popup(self):
        def content(frame):
            ttk.Label(frame, text="Delete Job", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
            # Add your delete job widgets here

        self.open_popup("Delete Job", content)

    def open_export_popup(self):
        def content(frame):
            ttk.Label(frame, text="Export All Jobs", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
            # Add your export widgets here

        self.open_popup("Export All Jobs", content)

    def open_credentials_popup(self):
        def content(frame):
            ttk.Label(frame, text="Settings", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

            ttk.Button(frame, text="Reset Credentials", command=reset_credentials, width=20).pack(pady=10)
            ttk.Button(frame, text="Delete Account", command=delete_account, width=20).pack(pady=(0, 20))

        def reset_credentials():
            self.app.show_frame('login')
            popup.destroy()

        def delete_account():
            if messagebox.askokcancel("Exit","Are you sure you want to delete your account? Everything will be lost forever."):
                self.app.user_manager.file_handler.delete_credentials()
                job_names = JobHandler.get_all_job_names()
                for name in job_names:
                    filename = f'jobs/{name}.json'
                    os.remove(filename)
                self.app.show_frame('login')
                popup.destroy()

        popup = self.open_popup("Change Credentials", content)

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.app.root.quit()
