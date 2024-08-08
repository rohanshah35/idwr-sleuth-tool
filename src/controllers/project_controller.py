import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import customtkinter as ctk

from src.fileio.exporter import ExcelExporter, CSVExporter
from src.fileio.file_handler import ProjectHandler
from src.structures.client import Client
from src.utils.constants import SUB_FRAME_WIDTH, SUB_FRAME_HEIGHT


class ProjectController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.project_label = ttk.Label(options_frame, text="", font=("Helvetica", 18, "bold"))
        self.project_label.pack(pady=(0, 30))

        self.select_client_btn = ctk.CTkButton(
            options_frame,
            text="Select Client",
            command=self.open_select_client_popup,
            width=140,
            height=30,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.select_client_btn.pack(pady=10)

        self.create_client_btn = ctk.CTkButton(
            options_frame,
            text="Create Client",
            command=self.open_create_client_popup,
            width=140,
            height=30,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.create_client_btn.pack(pady=10)

        self.delete_client_btn = ctk.CTkButton(
            options_frame,
            text="Delete Client",
            command=self.open_delete_client_popup,
            width=140,
            height=30,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.delete_client_btn.pack(pady=10)

        self.bulk_btn = ctk.CTkButton(
            options_frame,
            text="Send bulk message",
            command=self.open_bulk_popup,
            width=140,
            height=30,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.bulk_btn.pack(pady=10)

        self.export_btn = ctk.CTkButton(
            options_frame,
            text="Export",
            command=self.open_export_popup,
            width=140,
            height=30,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.export_btn.pack(pady=10)

        self.exit_btn = ctk.CTkButton(
            options_frame,
            text="Back to home",
            command=self.go_home,
            width=140,
            height=30,
            corner_radius=20,
            fg_color="#CC0000",
            hover_color="#990000"
        )
        self.exit_btn.pack(pady=(30, 10))

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_project()

    def hide(self):
        self.frame.pack_forget()

    def update_project(self):
        if self.app.selected_project:
            self.project_label.config(text=self.app.selected_project.name)

    def open_popup(self, title, content_func, width=SUB_FRAME_WIDTH, height=SUB_FRAME_HEIGHT):
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

        ctk.CTkButton(button_frame, text="Back", command=popup.destroy, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack()

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
        clients = self.app.selected_project.get_all_client_names()
        selected_client = tk.StringVar()
        selected_client.set(clients[0] if clients else "No clients available")

        def content(frame):
            ttk.Label(frame, text="Select Client", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ctk.CTkOptionMenu(frame, variable=selected_client, values=clients, width=140, fg_color="#2C3E50")
            drop.pack(pady=(30, 10))

            ctk.CTkButton(frame, text="Select Client", command=select_client, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def select_client():
            for client in self.app.client_list:
                if selected_client.get() == client.get_name():
                    self.app.selected_client = client
                    self.app.controllers['client'].update_client()
                    popup.destroy()
                    self.app.show_frame('client')

        popup = self.open_popup("Select Client", content)

    def open_create_client_popup(self):
        def content(frame):
            ttk.Label(frame, text="Create Client", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Label(frame, text="Client Name:").pack(pady=10)
            client_name_entry = ttk.Entry(frame, width=40)
            client_name_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Description:").pack(pady=10)
            client_desc_entry = tk.Text(frame, width=40, height=5)
            client_desc_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Company:").pack(pady=10)
            client_company_entry = ttk.Entry(frame, width=40)
            client_company_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client LinkedIn URL:").pack(pady=10)
            client_linkedin_entry = ttk.Entry(frame, width=40)
            client_linkedin_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Email:").pack(pady=10)
            client_email_entry = ttk.Entry(frame, width=40)
            client_email_entry.pack(pady=(0, 10), padx=20)

            create_button = ctk.CTkButton(
                frame,
                text="Create Client",
                command=lambda: create_client(client_name_entry.get(), client_desc_entry.get("1.0", tk.END), client_company_entry.get(), client_linkedin_entry.get(), client_email_entry.get()),
                width=140,
                height=30,
                corner_radius=20,
                fg_color="#2C3E50",
                hover_color="#1F2A38"
            )
            create_button.pack(pady=(20, 0))

        def create_client(client_name, client_description, client_company, client_linkedin, client_email):
            client = Client(client_name, client_description, client_company, client_linkedin, client_email)
            self.app.selected_project.add_client(client)
            project_manager = ProjectHandler(self.app.selected_project)
            project_manager.write_project()
            popup.destroy()
            messagebox.showinfo("Success", f"Client '{client_name}' created successfully!")

        popup = self.open_popup("Create Client", content)

    def open_delete_client_popup(self):
        clients = self.app.selected_job.get_all_client_names()
        selected_client = tk.StringVar()
        selected_client.set(clients[0] if clients else "No clients available")

        def content(frame):
            ttk.Label(frame, text="Delete Client", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ctk.CTkOptionMenu(frame, variable=selected_client, values=clients, width=140, fg_color="#2C3E50")
            drop.pack(pady=(30, 10))

            ctk.CTkButton(
                frame,
                text="Delete Client",
                command=delete_client,
                width=140,
                height=30,
                corner_radius=20,
                fg_color="#2C3E50",
                hover_color="#1F2A38"
            ).pack(pady=10)

        def delete_client():
            client_name = selected_client.get()
            clients.remove(client_name)
            self.app.selected_project.remove_client_by_name(selected_client.get())

            for client in self.app.client_list:
                if client.get_name() == client_name:
                    self.app.client_list.remove(client)

            project_manager = ProjectHandler(self.app.selected_project)
            project_manager.write_project()
            popup.destroy()
            messagebox.showinfo("Success", f"Client '{client_name}' deleted successfully!")

        popup = self.open_popup("Delete Client", content)

    def open_bulk_popup(self):
        self.app.show_frame('bulk')

    def open_export_popup(self):
        project_name = self.app.selected_project.get_name()

        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ctk.CTkButton(
                frame,
                text="Export Project (XLS)",
                command=export_xls,
                width=140,
                height=30,
                corner_radius=20,
                fg_color="#2C3E50",
                hover_color="#1F2A38"
            ).pack(pady=10)
            ctk.CTkButton(
                frame,
                text="Export Project (CSV)",
                command=export_csv,
                width=140,
                height=30,
                corner_radius=20,
                fg_color="#2C3E50",
                hover_color="#1F2A38"
            ).pack(pady=10)

        def export_xls():
            exporter = ExcelExporter()
            exporter.export_specific_project(self.app.selected_project.get_name())
            messagebox.showinfo("Export", f"Success, {project_name} exported successfully!")

        def export_csv():
            exporter = CSVExporter()
            exporter.export_specific_project(self.app.selected_project.get_name())
            messagebox.showinfo("Export", f"Success, {project_name} exported successfully!")

        self.open_popup("Export", content)

    def go_home(self):
        self.app.show_frame('home')
