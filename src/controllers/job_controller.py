import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

from src.fileio.exporter import ExcelExporter, CSVExporter
from src.fileio.file_handler import JobHandler
from src.structures.client import Client


class JobController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        # Options frame
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.job_label = ttk.Label(options_frame, text="", font=("Helvetica", 18, "bold"))
        self.job_label.pack(pady=(0, 30))

        self.select_client_btn = ttk.Button(options_frame, text="Select Client", command=self.open_select_client_popup, width=20)
        self.select_client_btn.pack(pady=10)

        self.create_client_btn = ttk.Button(options_frame, text="Create Client", command=self.open_create_client_popup, width=20)
        self.create_client_btn.pack(pady=10)

        self.delete_client_btn = ttk.Button(options_frame, text="Delete Client", command=self.open_delete_client_popup, width=20)
        self.delete_client_btn.pack(pady=10)

        self.bulk_btn = ttk.Button(options_frame, text="Send bulk message", command=self.open_bulk_popup, width=20)
        self.bulk_btn.pack(pady=10)

        self.export_btn = ttk.Button(options_frame, text="Export", command=self.open_export_popup, width=20)
        self.export_btn.pack(pady=10)

        self.exit_btn = ttk.Button(options_frame, text="Back to home", command=self.go_home, width=20)
        self.exit_btn.pack(pady=(30, 10))

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_job()

    def hide(self):
        self.frame.pack_forget()

    def update_job(self):
        if self.app.selected_job:
            self.job_label.config(text=self.app.selected_job.name)

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

    def open_select_client_popup(self):
        clients = self.app.selected_job.get_all_client_names()
        selected_client = tk.StringVar()
        selected_client.set(clients[0] if clients else "No clients available")

        def content(frame):
            ttk.Label(frame, text="Select Client", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ttk.OptionMenu(frame, selected_client, selected_client.get(), *clients)
            drop.pack(pady=10)

            ttk.Button(frame, text="Select Client", command=select_client, width=20).pack(pady=10)

        def select_client():
            for client in self.app.client_list:
                if selected_client.get() == client.get_name():
                    self.app.selected_client = client
                    self.app.controllers['client'].update_client()
                    popup.destroy()
                    self.app.show_frame('client')

        popup = self.open_popup("Select Job", content)

    def open_create_client_popup(self):
        def content(frame):
            ttk.Label(frame, text="Create Client", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Label(frame, text="Client Name:").pack(pady=10)
            client_name_entry = ttk.Entry(frame, width=40)
            client_name_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Description:").pack(pady=10)
            client_desc_entry = tk.Text(frame, width=40, height=5)
            client_desc_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client LinkedIn URL:").pack(pady=10)
            client_linkedin_entry = ttk.Entry(frame, width=40)
            client_linkedin_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Email:").pack(pady=10)
            client_email_entry = ttk.Entry(frame, width=40)
            client_email_entry.pack(pady=(0, 10), padx=20)

            create_button = ttk.Button(frame, text="Create Client", command=lambda: create_client(client_name_entry.get(), client_desc_entry.get("1.0", tk.END), client_linkedin_entry.get(), client_email_entry.get()))
            create_button.pack(pady=(20, 0))

        def create_client(client_name, client_description, client_linkedin, client_email):
            client = Client(client_name, client_description, client_linkedin, client_email)
            self.app.selected_job.add_client(client)
            job_manager = JobHandler(self.app.selected_job)
            job_manager.write_job()
            popup.destroy()
            messagebox.showinfo("Success", f"Client '{client_name}' created successfully!")

        popup = self.open_popup("Create Client", content)

    def open_delete_client_popup(self):
        clients = self.app.selected_job.get_all_client_names()
        selected_client = tk.StringVar()
        selected_client.set(clients[0] if clients else "No clients available")

        def content(frame):
            ttk.Label(frame, text="Delete Client", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ttk.OptionMenu(frame, selected_client, selected_client.get(), *clients)
            drop.pack(pady=10)

            ttk.Button(frame, text="Delete Client", command=delete_client, width=20).pack(pady=10)

        def delete_client():
            client_name = selected_client.get()
            clients.remove(client_name)
            self.app.selected_job.remove_client_by_name(selected_client)

            for client in self.app.client_list:
                if client.get_name() == client_name:
                    self.app.client_list.remove(client)

            job_manager = JobHandler(self.app.selected_job)
            job_manager.write_job()
            popup.destroy()
            messagebox.showinfo("Success", f"Client '{client_name}' deleted successfully!")

        popup = self.open_popup("Delete Client", content)

    def open_bulk_popup(self):
        def content(frame):
            ttk.Label(frame, text="Send Bulk Message", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

        self.open_popup("Send Bulk Message", content)

    def open_export_popup(self):
        job_name = self.app.selected_job.get_name()

        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Button(frame, text="Export Job (XLS)", command=export_xls, width=20).pack(pady=10)
            ttk.Button(frame, text="Export Job (CSV)", command=export_csv, width=20).pack(pady=10)

        def export_xls():
            exporter = ExcelExporter()
            exporter.export_specific_job(self.app.selected_job.get_name())
            messagebox.showinfo(f"Success, f'{job_name} exported successfully!")

        def export_csv():
            exporter = CSVExporter()
            exporter.export_specific_job(self.app.selected_job.get_name())
            messagebox.showinfo(f"Success, f'{job_name} exported successfully!")

        self.open_popup("Export", content)

    def go_home(self):
        self.app.show_frame('home')
