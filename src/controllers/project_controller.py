# Handles project menu within GUI

import threading
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import customtkinter as ctk

from src.fileio.exporter import ExcelExporter, CSVExporter
from src.fileio.file_handler import ProjectHandler
from src.structures.client import Client
from src.utils.constants import SUB_FRAME_WIDTH, SUB_FRAME_HEIGHT
from src.utils.utils import DateEntry


class ProjectController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.project_label = ttk.Label(options_frame, text="", font=("Helvetica", 18, "bold"))
        self.project_label.pack(pady=(0, 30))

        self.edit_project_btn = ctk.CTkButton(
            options_frame,
            text="Edit Project",
            command=self.open_edit_project_popup,
            width=140,
            height=30,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.edit_project_btn.pack(pady=(10, 30))

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
            text="Back",
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
            self.project_label.config(text=self.app.selected_project.get_name())

    def update_project_label(self):
        if self.app.selected_project:
            self.project_label.config(text=self.app.selected_project.get_name())

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

    def open_edit_project_popup(self):
        def content(frame):
            ttk.Label(frame, text="Edit Project", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Label(frame, text="Project Name:").pack(pady=10)
            project_name_entry = ttk.Entry(frame, width=40)
            project_name_entry.insert(0, self.app.selected_project.get_name())
            project_name_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Project Description:").pack(pady=10)
            project_desc_entry = tk.Text(frame, width=40, height=5)
            project_desc_entry.insert("1.0", self.app.selected_project.get_description())
            project_desc_entry.pack(pady=(0, 20), padx=20)

            create_button = ctk.CTkButton(frame, text="Save Project", command=lambda: edit_project(project_name_entry.get(), project_desc_entry.get("1.0", tk.END).strip()), width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
            create_button.pack(pady=(0, 30))

        def edit_project(new_name, new_description):
            project_handler = ProjectHandler(self.app.selected_project)
            old_name = self.app.selected_project.get_name()

            if new_name and new_name != old_name:
                self.app.selected_project.set_name(new_name)
                project_handler.rename_project(new_name)

            if new_description and new_description != self.app.selected_project.get_description():
                self.app.selected_project.set_description(new_description)

            project_handler.write_project()

            self.update_project_label()

            popup.destroy()
            messagebox.showinfo("Success", f"Project '{self.app.selected_project.get_name()}' edited successfully!")

        popup = self.open_popup("Edit Project", content)

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
            ttk.Label(frame, text="Create Client", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

            anonymous_var = tk.BooleanVar()

            def toggle_anonymous():
                if anonymous_var.get():
                    client_name_entry.delete(0, tk.END)
                    client_name_entry.insert(0, "Anonymous")
                    client_name_entry.config(state="disabled")
                else:
                    client_name_entry.config(state="normal")
                    client_name_entry.delete(0, tk.END)

            anonymous_check = ttk.Checkbutton(frame, text="Anonymous Client", variable=anonymous_var, command=toggle_anonymous)
            anonymous_check.pack(pady=(0, 10))

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
                command=lambda: self.create_client(
                    client_name_entry.get(),
                    client_desc_entry.get("1.0", tk.END),
                    client_company_entry.get(),
                    client_linkedin_entry.get(),
                    client_email_entry.get(),
                    anonymous_var.get()
                ),
                width=140,
                height=30,
                corner_radius=20,
                fg_color="#2C3E50",
                hover_color="#1F2A38"
            )
            create_button.pack(pady=(20, 0))

        self.popup = self.open_popup("Create Client", content)

    def create_client(self, client_name, client_description, client_company, client_linkedin, client_email, anonymous):
        # Disable the create button to prevent multiple submissions
        for widget in self.popup.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Create Client":
                widget.configure(state="disabled")

        # Show a loading message
        loading_label = ttk.Label(self.popup, text="Creating client...", font=("Helvetica", 12))
        loading_label.pack(pady=10)

        # Start a new thread for client creation
        threading.Thread(target=self._create_client_thread,
                         args=(client_name, client_description, client_company, client_linkedin, client_email, anonymous),
                         daemon=True).start()

    def _create_client_thread(self, client_name, client_description, client_company, client_linkedin, client_email, anonymous):
        try:
            if client_linkedin:
                client_linkedin_name = self.app.user_manager.get_linkedin_handler().get_linkedin_profile_name(client_linkedin)
                client = Client(client_name, client_description, client_company, client_linkedin, client_email, anonymous, client_linkedin_name)
            else:
                client = Client(client_name, client_description, client_company, client_linkedin, client_email, anonymous)

            self.app.selected_project.add_client(client)
            self.app.update_entire_client_list()
            project_manager = ProjectHandler(self.app.selected_project)
            project_manager.write_project()

            # Schedule UI updates on the main thread
            self.app.root.after(0, self._finish_client_creation, client_name)
        except Exception as e:
            # Schedule error handling on the main thread
            self.app.root.after(0, self._handle_client_creation_error, str(e))

    def _finish_client_creation(self, client_name):
        self.popup.destroy()
        messagebox.showinfo("Success", f"Client '{client_name}' created successfully!")

    def _handle_client_creation_error(self, error_message):
        # Remove the loading message
        for widget in self.popup.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("text") == "Creating client...":
                widget.destroy()

        # Re-enable the create button
        for widget in self.popup.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Create Client":
                widget.configure(state="normal")

        messagebox.showinfo("Error", f"Failed to create client: {error_message}")


    def open_delete_client_popup(self):
        clients = self.app.selected_project.get_all_client_names()
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

            self.app.update_entire_client_list()
            project_manager = ProjectHandler(self.app.selected_project)
            project_manager.write_project()
            popup.destroy()
            messagebox.showinfo("Success", f"Client '{client_name}' deleted successfully!")

        popup = self.open_popup("Delete Client", content)

    def open_bulk_popup(self):
        self.app.show_frame('bulk')

    def open_export_popup(self):
        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

            # Start Date
            ttk.Label(frame, text="Start Date:").pack(pady=(10, 5))
            start_date = DateEntry(frame)
            start_date.pack(pady=(0, 10))

            # End Date
            ttk.Label(frame, text="End Date:").pack(pady=(10, 5))
            end_date = DateEntry(frame)
            end_date.pack(pady=(0, 20))

            ctk.CTkButton(frame, text="Export Selected Project (XLSX)",
                          command=lambda: export_xls(start_date.get_date(), end_date.get_date()),
                          width=200, height=30, corner_radius=20,
                          fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

            ctk.CTkButton(frame, text="Export Selected Project (CSV)",
                          command=lambda: export_csv(start_date.get_date(), end_date.get_date()),
                          width=200, height=30, corner_radius=20,
                          fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def export_xls(start_date, end_date):
            exporter = ExcelExporter()
            output = exporter.export_specific_project(self.app.selected_project.get_name(), start_date, end_date)
            if output is None:
                messagebox.showinfo("Error", "No data found within selected timeframe!")
            else:
                messagebox.showinfo("Export", "Success, project exported successfully!")

        def export_csv(start_date, end_date):
            exporter = CSVExporter()
            output = exporter.export_specific_project(self.app.selected_project.get_name(), start_date, end_date)
            if output is None:
                messagebox.showinfo("Error", "No data found within selected timeframe!")
            else:
                messagebox.showinfo("Export", "Success, project exported successfully!")

        self.open_popup("Export", content)

    def go_home(self):
        self.app.show_frame('home')
