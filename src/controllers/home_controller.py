import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk  # Make sure to import customtkinter

from src.fileio.file_handler import JobHandler
from src.structures.job import Job
from src.fileio.exporter import ExcelExporter, CSVExporter


class HomeController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        self.app.user_manager.load_handlers()

        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.welcome_frame = ttk.Frame(options_frame)
        self.welcome_frame.pack(pady=(0, 40))

        self.greeting_label = ttk.Label(self.welcome_frame, text="Welcome to IDWR Office, ", font=("Helvetica", 18))
        self.greeting_label.pack(side=tk.LEFT)

        self.email_label = ttk.Label(self.welcome_frame, text="", font=("Helvetica", 18, "bold"))
        self.email_label.pack(side=tk.LEFT)

        original_image = Image.open("resources/mailbox.png")
        resized_image = original_image.resize((30, 30), Image.LANCZOS)
        self.mailbox_image = ImageTk.PhotoImage(resized_image)

        self.mailbox_btn = ctk.CTkButton(
            options_frame,
            text="Messages",
            image=self.mailbox_image,
            compound=tk.LEFT,
            command=self.open_mailbox_popup,
            width=142,
            height=30,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.mailbox_btn.pack(pady=(10, 30))

        self.select_job_btn = ctk.CTkButton(options_frame, text="Select Job", command=self.open_select_job_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.select_job_btn.pack(pady=10)

        self.create_job_btn = ctk.CTkButton(options_frame, text="Create Job", command=self.open_create_job_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.create_job_btn.pack(pady=10)

        self.delete_job_btn = ctk.CTkButton(options_frame, text="Delete Job", command=self.open_delete_job_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.delete_job_btn.pack(pady=10)

        self.export_btn = ctk.CTkButton(options_frame, text="Export", command=self.open_export_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.export_btn.pack(pady=10)

        self.account_cred_btn = ctk.CTkButton(options_frame, text="Settings", command=self.open_credentials_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.account_cred_btn.pack(pady=(30, 10))

        self.exit_btn = ctk.CTkButton(options_frame, text="Exit", command=self.exit_app, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.exit_btn.pack(pady=10)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_email()

    def hide(self):
        self.frame.pack_forget()

    def update_email(self):
        email = self.app.user_manager.user_data.get('linkedin_username', 'Not set')
        self.email_label.config(text=email+'!')

    def open_mailbox_popup(self):
        messagebox.showinfo("Mailbox", "Mailbox clicked!")

    def open_popup(self, title, content_func, width=1000, height=800):
        popup = tk.Toplevel(self.app.root)
        popup.title(title)
        popup.geometry(f"{width}x{height}")
        popup.transient(self.app.root)
        popup.grab_set()
        popup.resizable(False, False)

        self.center_popup(popup, width, height)

        content_frame = ttk.Frame(popup, padding="20 20 20 20")
        content_frame.pack(fill=tk.BOTH, expand=True)

        content_func(content_frame)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(side=BOTTOM, fill=X, pady=10)

        ctk.CTkButton(button_frame, text="Back", command=popup.destroy, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=5)

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
        jobs = JobHandler.get_all_job_names()
        selected_job = tk.StringVar()
        selected_job.set(jobs[0] if jobs else "No jobs available")

        def content(frame):
            ttk.Label(frame, text="Select Job", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ctk.CTkOptionMenu(frame, variable=selected_job, values=jobs, width=140, fg_color="#2C3E50")
            drop.pack(pady=(30, 10))

            ctk.CTkButton(frame, text="Select Job", command=select_job, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def select_job():
            for job in self.app.job_list:
                if selected_job.get() == job.get_name():
                    self.app.selected_job = job
                    self.app.client_list = job.get_clients()
                    self.app.controllers['job'].update_job()
                    popup.destroy()
                    self.app.show_frame('job')

        popup = self.open_popup("Select Job", content)

    def open_create_job_popup(self):
        def content(frame):
            ttk.Label(frame, text="Create Job", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Label(frame, text="Job Name:").pack(pady=10)
            job_name_entry = ttk.Entry(frame, width=40)
            job_name_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Job Description:").pack(pady=10)
            job_desc_entry = tk.Text(frame, width=40, height=5)
            job_desc_entry.pack(pady=(0, 20), padx=20)

            create_button = ctk.CTkButton(frame, text="Create Job", command=lambda: create_job(job_name_entry.get(), job_desc_entry.get("1.0", tk.END)), width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
            create_button.pack(pady=(0, 30))

        def create_job(job_name, job_description):
            job = Job(job_name, job_description)
            self.app.job_list.append(job)
            job_handler = JobHandler(job)
            job_handler.write_job()
            popup.destroy()
            messagebox.showinfo("Success", f"Job '{job_name}' created successfully!")

        popup = self.open_popup("Create Job", content)

    def open_delete_job_popup(self):
        jobs = JobHandler.get_all_job_names()
        selected_job = tk.StringVar()
        selected_job.set(jobs[0] if jobs else "No jobs available")

        def content(frame):
            ttk.Label(frame, text="Delete Job", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ctk.CTkOptionMenu(frame, variable=selected_job, values=jobs, width=140, fg_color="#2C3E50")
            drop.pack(pady=(30, 10))

            ctk.CTkButton(frame, text="Delete Job", command=delete_job, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def delete_job():
            job_name = selected_job.get()
            filename = f'jobs/{job_name}.json'
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    popup.destroy()
                    messagebox.showinfo("Success", f"Job '{job_name}' deleted successfully!")
                    jobs.remove(job_name)

                    for job in self.app.job_list:
                        if job.get_name() == job_name:
                            self.app.job_list.remove(job)
                except OSError as e:
                    print(f"Error deleting job file: {e}")
            else:
                print(f"Job file '{filename}' does not exist.")

        popup = self.open_popup("Delete Job", content)

    def open_export_popup(self):
        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ctk.CTkButton(frame, text="Export All Jobs (XLS)", command=export_xls, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Export All Jobs (CSV)", command=export_csv, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def export_xls():
            exporter = ExcelExporter()
            exporter.export_all_jobs()
            messagebox.showinfo("Export", "Success, all jobs exported successfully!")

        def export_csv():
            exporter = CSVExporter()
            exporter.export_all_jobs()
            messagebox.showinfo("Export", "Success, all jobs exported successfully!")

        self.open_popup("Export", content)

    def open_credentials_popup(self):
        def content(frame):
            ttk.Label(frame, text="Settings", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ctk.CTkButton(frame, text="Reset Credentials", command=reset_credentials, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Delete Account", command=delete_account, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def reset_credentials():
            if messagebox.askokcancel("Reset Credentials", "Are you sure you want to reset your credentials?"):
                self.app.show_frame('login')
                popup.destroy()

        def delete_account():
            if messagebox.askokcancel("Delete Account", "Are you sure you want to delete your account? Everything will be lost forever."):
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
