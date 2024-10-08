# Handles home menu within GUI

import threading
import os
import tkinter as tk
from queue import Queue, Empty
import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import customtkinter as ctk

from src.fileio.file_handler import ProjectHandler
from src.structures.project import Project
from src.fileio.exporter import ExcelExporter, CSVExporter
from src.utils.constants import SUB_FRAME_WIDTH, SUB_FRAME_HEIGHT
from src.utils.utils import DateEntry


class HomeController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.welcome_frame = ttk.Frame(options_frame)
        self.welcome_frame.pack(pady=(0, 40))

        self.greeting_label = ttk.Label(self.welcome_frame, text="Welcome to IDWR Office, ", font=("Helvetica", 18))
        self.greeting_label.pack(side=tk.LEFT)

        self.email_label = ttk.Label(self.welcome_frame, text="", font=("Helvetica", 18, "bold"))
        self.email_label.pack(side=tk.LEFT)

        self.mailbox_btn = ctk.CTkButton(
            options_frame,
            text="Notifications",
            command=self.open_mailbox_popup,
            width=140,
            height=32,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.mailbox_btn.pack(pady=(10, 30))

        self.select_project_btn = ctk.CTkButton(options_frame, text="Select Project",
                                                command=self.open_select_project_popup, width=140, height=30,
                                                corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.select_project_btn.pack(pady=10)

        self.create_project_btn = ctk.CTkButton(options_frame, text="Create Project",
                                                command=self.open_create_project_popup, width=140, height=30,
                                                corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.create_project_btn.pack(pady=10)

        self.delete_project_btn = ctk.CTkButton(options_frame, text="Delete Project",
                                                command=self.open_delete_project_popup, width=140, height=30,
                                                corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.delete_project_btn.pack(pady=10)

        self.export_btn = ctk.CTkButton(options_frame, text="Export", command=self.open_export_popup, width=140,
                                        height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.export_btn.pack(pady=10)

        self.account_cred_btn = ctk.CTkButton(options_frame, text="Settings", command=self.open_settings_popup,
                                              width=140, height=30, corner_radius=20, fg_color="#606060",
                                              hover_color="#505050")
        self.account_cred_btn.pack(pady=(30, 10))

        self.exit_btn = ctk.CTkButton(options_frame, text="Exit", command=self.exit_app, width=140, height=30,
                                      corner_radius=20, fg_color="#CC0000", hover_color="#990000")
        self.exit_btn.pack(pady=10)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_email()

    def hide(self):
        self.frame.pack_forget()

    def update_email(self):
        email = self.app.user_manager.get_user_data().get('linkedin_email', 'Not set')
        self.email_label.config(text=email + '!')

    def open_mailbox_popup(self):
        popup = self.open_popup("Mailbox", self.loading_content)
        progress_var, status_var = self.get_progress_vars(popup)

        def fetch_data():
            try:
                queue = Queue()
                threading.Thread(target=fetch_data_thread, args=(queue,), daemon=True).start()
                update_progress(popup, queue, progress_var, status_var)
            except Exception as e:
                self.app.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))

        def fetch_data_thread(queue):
            queue.put(("status", "Checking LinkedIn messages..."))
            linkedin_messages = self.app.user_manager.get_linkedin_handler().check_for_new_messages(
                self.app.entire_client_list)
            queue.put(("progress", 50))

            queue.put(("status", "Checking emails..."))
            new_emails = self.app.user_manager.get_email_handler().search_mailbox_for_unseen_emails_from_clients(
                self.app.entire_client_list)
            queue.put(("progress", 100))

            for client in linkedin_messages:
                client.set_has_responded(True)
            for client in new_emails:
                client.set_has_responded(True)

            for project in self.app.project_list:
                project_manager = ProjectHandler(project)
                project_manager.write_project()

            queue.put(("done", (linkedin_messages, new_emails)))

        def update_progress(popup, queue, progress_var, status_var):
            try:
                message = queue.get_nowait()
                if message[0] == "progress":
                    progress_var.set(message[1])
                elif message[0] == "status":
                    status_var.set(message[1])
                elif message[0] == "done":
                    linkedin_messages, new_emails = message[1]
                    self.app.root.after(0, lambda: self.update_mailbox_ui(popup, linkedin_messages, new_emails))
                    return
                popup.after(100, update_progress, popup, queue, progress_var, status_var)
            except Empty:
                popup.after(100, update_progress, popup, queue, progress_var, status_var)

        fetch_data()

    def loading_content(self, frame):
        ttk.Label(frame, text="Loading notifications...", font=("Helvetica", 16, "bold")).pack(pady=20)

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
        progress_bar.pack(pady=10, padx=20, fill=tk.X)

        status_var = tk.StringVar()
        status_label = ttk.Label(frame, textvariable=status_var)
        status_label.pack(pady=5)

        frame.progress_var = progress_var
        frame.status_var = status_var

    def get_progress_vars(self, popup):
        for child in popup.winfo_children():
            if hasattr(child, 'progress_var') and hasattr(child, 'status_var'):
                return child.progress_var, child.status_var
        return None, None

    def update_mailbox_ui(self, popup, linkedin_messages, new_emails):
        for widget in popup.winfo_children():
            widget.destroy()

        self.create_mailbox_content(popup, linkedin_messages, new_emails)

    def create_mailbox_content(self, popup, linkedin_messages, new_emails):
        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Notifications", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        linkedin_frame = ttk.Frame(notebook)
        notebook.add(linkedin_frame, text="LinkedIn Messages")

        if linkedin_messages:
            for client in linkedin_messages:
                message_frame = ttk.Frame(linkedin_frame)
                message_frame.pack(fill=tk.X, padx=5, pady=5)
                ttk.Label(message_frame, text=f"New message from: {client.get_name()}",
                          font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
                ttk.Label(message_frame, text=f"Company: {client.get_company()}").pack(anchor=tk.W)
                ttk.Separator(linkedin_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=5)
        else:
            ttk.Label(linkedin_frame, text="No new LinkedIn messages").pack(pady=20)

        email_frame = ttk.Frame(notebook)
        notebook.add(email_frame, text="Emails")

        if new_emails:
            for client in new_emails:
                email_message_frame = ttk.Frame(email_frame)
                email_message_frame.pack(fill=tk.X, padx=5, pady=5)
                ttk.Label(email_message_frame, text=f"New email from: {client.get_name()}",
                          font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
                ttk.Label(email_message_frame, text=f"Email: {client.get_email()}").pack(anchor=tk.W)
                ttk.Separator(email_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=5)
        else:
            ttk.Label(email_frame, text="No new emails").pack(pady=20)

        button_frame = ttk.Frame(frame)
        button_frame.pack(side=BOTTOM, fill=X, pady=10)

        ctk.CTkButton(button_frame, text="Back", command=popup.destroy, corner_radius=20, fg_color="#2C3E50",
                      hover_color="#1F2A38").pack(pady=5)

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

        ctk.CTkButton(button_frame, text="Back", command=popup.destroy, corner_radius=20, fg_color="#2C3E50",
                      hover_color="#1F2A38").pack(pady=5)

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

    def open_select_project_popup(self):
        projects = ProjectHandler.get_all_project_names()
        selected_project = tk.StringVar()
        selected_project.set(projects[0] if projects else "No projects available")

        def content(frame):
            ttk.Label(frame, text="Select Project", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ctk.CTkOptionMenu(frame, variable=selected_project, values=projects, width=140, fg_color="#2C3E50")
            drop.pack(pady=(30, 10))

            ctk.CTkButton(frame, text="Select Project", command=select_project, width=140, height=30, corner_radius=20,
                          fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def select_project():
            for project in self.app.project_list:
                if selected_project.get() == project.get_name():
                    self.app.selected_project = project
                    self.app.client_list = project.get_clients()
                    self.app.controllers['project'].update_project()
                    popup.destroy()
                    self.app.show_frame('project')

        popup = self.open_popup("Select Project", content)

    def open_create_project_popup(self):
        def content(frame):
            ttk.Label(frame, text="Create Project", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Label(frame, text="Project Name:").pack(pady=10)
            project_name_entry = ttk.Entry(frame, width=40)
            project_name_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Project Description:").pack(pady=10)
            project_desc_entry = tk.Text(frame, width=40, height=5)
            project_desc_entry.pack(pady=(0, 20), padx=20)

            create_button = ctk.CTkButton(frame, text="Create Project",
                                          command=lambda: create_project(project_name_entry.get(),
                                                                         project_desc_entry.get("1.0", tk.END)),
                                          width=140, height=30, corner_radius=20, fg_color="#2C3E50",
                                          hover_color="#1F2A38")
            create_button.pack(pady=(0, 30))

        def create_project(project_name, project_description):
            project = Project(project_name, project_description)
            self.app.project_list.append(project)
            project_handler = ProjectHandler(project)
            project_handler.write_project()
            popup.destroy()
            messagebox.showinfo("Success", f"Project '{project_name}' created successfully!")

        popup = self.open_popup("Create Project", content)

    def open_delete_project_popup(self):
        projects = ProjectHandler.get_all_project_names()
        selected_project = tk.StringVar()
        selected_project.set(projects[0] if projects else "No projects available")

        def content(frame):
            ttk.Label(frame, text="Delete Project", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ctk.CTkOptionMenu(frame, variable=selected_project, values=projects, width=140, fg_color="#2C3E50")
            drop.pack(pady=(30, 10))

            ctk.CTkButton(frame, text="Delete Project", command=delete_project, width=140, height=30, corner_radius=20,
                          fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def delete_project():
            project_name = selected_project.get()
            filename = f'projects/{project_name}.json'
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    self.app.update_project_list()
                    popup.destroy()
                    messagebox.showinfo("Success", f"Project '{project_name}' deleted successfully!")
                except OSError as e:
                    messagebox.showerror("Error", f"Error deleting project '{project_name}': {e}")
            else:
                messagebox.showerror("Error", f"Project '{project_name}' not found.")

        popup = self.open_popup("Delete Project", content)

    def open_export_popup(self):
        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

            ttk.Label(frame, text="Start Date:").pack(pady=(10, 5))
            start_date = DateEntry(frame)
            start_date.pack(pady=(0, 10))

            ttk.Label(frame, text="End Date:").pack(pady=(10, 5))
            end_date = DateEntry(frame)
            end_date.pack(pady=(0, 20))

            ctk.CTkButton(frame, text="Export All Projects (XLSX)",
                          command=lambda: export_xls(start_date.get_date(), end_date.get_date()),
                          width=200, height=30, corner_radius=20,
                          fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

            ctk.CTkButton(frame, text="Export All Projects (CSV)",
                          command=lambda: export_csv(start_date.get_date(), end_date.get_date()),
                          width=200, height=30, corner_radius=20,
                          fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def export_xls(start_date, end_date):
            exporter = ExcelExporter()
            exporter.export_all_projects(start_date, end_date)
            messagebox.showinfo("Export", "Success, all projects exported successfully!")

        def export_csv(start_date, end_date):
            exporter = CSVExporter()
            exporter.export_all_projects(start_date, end_date)
            messagebox.showinfo("Export", "Success, all projects exported successfully!")

        self.open_popup("Export", content)

    def open_settings_popup(self):
        def content(frame):
            ttk.Label(frame, text="Settings", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ctk.CTkButton(frame, text="Reset Credentials", command=reset_credentials, width=140, height=30,
                          corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Delete Account", command=delete_account, width=140, height=30, corner_radius=20,
                          fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Instructions", command=show_instructions, width=140, height=30, corner_radius=20,
                          fg_color="#805500", hover_color="#664400").pack(pady=(30, 10))
            ctk.CTkButton(frame, text="Submit Bug Ticket", command=show_bug_ticket, width=140, height=30,
                          corner_radius=20, fg_color="#446600", hover_color="#334d00").pack(pady=10)

        def reset_credentials():
            if messagebox.askokcancel("Reset Credentials", "Are you sure you want to reset your credentials?"):
                self.app.show_frame('login')
                popup.destroy()

        def delete_account():
            if messagebox.askokcancel("Delete Account",
                                      "Are you sure you want to delete your account? Everything will be lost forever."):
                self.app.user_manager.get_file_handler().delete_credentials()
                project_names = ProjectHandler.get_all_project_names()
                for name in project_names:
                    filename = f'projects/{name}.json'
                    os.remove(filename)
                self.app.show_frame('login')
                popup.destroy()

        def show_instructions():
            def content(frame):
                ttk.Label(frame, text="Instructions", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

                instructions = [
                    "I. Home Menu",
                    "   A. Select Project: Choose which project to work on",
                    "   B. Create Project: Create a project, with a name and description",
                    "   C. Delete Project: Delete a project (forever)",
                    "   D. Export: Export a full report, includes all projects and clients",
                    "",
                    "II. Project Menu",
                    "   A. Select Client: Choose which client to work on",
                    "   B. Create Client: Create a client, with a name, description, company, LinkedIn URL, and email",
                    "   C. Delete Client: Delete a client (forever)",
                    "   D. Send bulk message: Send a bulk message (either LinkedIn or email) to clients of your choosing",
                    "   E. Export: Export a project report, includes all clients",
                    "",
                    "III. Client Menu",
                    "   A. LinkedIn Conversation: Send a LinkedIn message to client",
                    "   B. Email Conversation: Send an email to client",
                    "   C. Export: Export a client report, includes all client attributes",
                    "",
                    "IV. Settings",
                    "   A. Reset Credentials: In the case your login changes to LinkedIn and/or email, you can reset your credentials without losing any data",
                    "   B. Delete Account: Wipe all data, including credentials, forever",
                    "",
                ]

                for instruction in instructions:
                    ttk.Label(frame, text=instruction, font=("Arial", 10)).pack(anchor=tk.W, padx=20)

                ttk.Label(frame, text="Any more questions? Contact email@gmail.com",
                          font=("Helvetica", 10, "italic")).pack(pady=(90, 0))

            self.open_popup("Instructions", content)

        def show_bug_ticket():
            def content(frame):
                ttk.Label(frame, text="Bug Ticket Submission", font=("Helvetica", 16, "bold")).pack(pady=(0, 40))

                ticket_entry = tk.Text(frame, width=80, height=20)
                ticket_entry.pack(pady=(0, 20), padx=20)

                send_button = ctk.CTkButton(frame, text="Submit Ticket",
                                            command=lambda: submit_ticket(ticket_entry.get("1.0", tk.END)), width=140,
                                            height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
                send_button.pack(pady=(0, 30))

                def submit_ticket(ticket):
                    webhook_url = "https://discord.com/api/webhooks/1272445421943390272/tLSoAlr0hI1zjJiDzsVFmsbC8R11rHtQalh7AzxrpxJ4gP_zcIjMyku3Ca-ZK5ktnK5l"

                    data = {
                        "content": "New Bug Ticket Submission",
                        "embeds": [{
                            "title": "IDWR Intern Bug Ticket",
                            "description": ticket,
                            "color": 15158332
                        }]
                    }

                    response = requests.post(webhook_url, json=data)

                    if response.status_code == 204:
                        popup.destroy()
                        messagebox.showinfo("Success", "Ticket submitted successfully!")
                    else:
                        messagebox.showerror("Error", f"Failed to submit ticket. Status code: {response.status_code}")

            self.open_popup("Bug Ticket Submission", content)

        popup = self.open_popup("Settings", content)

    def exit_app(self):
        self.app.root.destroy()
