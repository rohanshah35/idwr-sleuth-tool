import os
import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk

from src.fileio.file_handler import ProjectHandler
from src.structures.project import Project
from src.fileio.exporter import ExcelExporter, CSVExporter
from src.utils.constants import SUB_FRAME_WIDTH, SUB_FRAME_HEIGHT


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
        resized_image = original_image.resize((20, 20), Image.LANCZOS)

        self.mailbox_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(20, 20))

        self.mailbox_btn = ctk.CTkButton(
            options_frame,
            text="Notifications",
            image=self.mailbox_image,
            compound="left",
            command=self.open_mailbox_popup,
            width=140,
            height=32,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.mailbox_btn.pack(pady=(10, 30))

        self.select_project_btn = ctk.CTkButton(options_frame, text="Select Project", command=self.open_select_project_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.select_project_btn.pack(pady=10)

        self.create_project_btn = ctk.CTkButton(options_frame, text="Create Project", command=self.open_create_project_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.create_project_btn.pack(pady=10)

        self.delete_project_btn = ctk.CTkButton(options_frame, text="Delete Project", command=self.open_delete_project_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.delete_project_btn.pack(pady=10)

        self.export_btn = ctk.CTkButton(options_frame, text="Export", command=self.open_export_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.export_btn.pack(pady=10)

        self.account_cred_btn = ctk.CTkButton(options_frame, text="Settings", command=self.open_settings_popup, width=140, height=30, corner_radius=20, fg_color="#606060", hover_color="#505050")
        self.account_cred_btn.pack(pady=(30, 10))

        self.exit_btn = ctk.CTkButton(options_frame, text="Exit", command=self.exit_app, width=140, height=30, corner_radius=20, fg_color="#CC0000", hover_color="#990000")
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

    def open_select_project_popup(self):
        projects = ProjectHandler.get_all_project_names()
        selected_project = tk.StringVar()
        selected_project.set(projects[0] if projects else "No projects available")

        def content(frame):
            ttk.Label(frame, text="Select Project", font=("Helvetica", 16, "bold")).pack(pady=10)

            drop = ctk.CTkOptionMenu(frame, variable=selected_project, values=projects, width=140, fg_color="#2C3E50")
            drop.pack(pady=(30, 10))

            ctk.CTkButton(frame, text="Select Project", command=select_project, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

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

            create_button = ctk.CTkButton(frame, text="Create Project", command=lambda: create_project(project_name_entry.get(), project_desc_entry.get("1.0", tk.END)), width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
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

            ctk.CTkButton(frame, text="Delete Project", command=delete_project, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def delete_project():
            project_name = selected_project.get()
            filename = f'projects/{project_name}.json'
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    popup.destroy()
                    messagebox.showinfo("Success", f"Project '{project_name}' deleted successfully!")
                except OSError as e:
                    messagebox.showerror("Error", f"Error deleting project '{project_name}': {e}")
            else:
                messagebox.showerror("Error", f"Project '{project_name}' not found.")

        popup = self.open_popup("Delete Project", content)

    def open_export_popup(self):
        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ctk.CTkButton(frame, text="Export All Projects (XLS)", command=export_xls, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Export All Projects (CSV)", command=export_csv, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def export_xls():
            exporter = ExcelExporter()
            exporter.export_all_projects()
            messagebox.showinfo("Export", "Success, all projects exported successfully!")

        def export_csv():
            exporter = CSVExporter()
            exporter.export_all_projects()
            messagebox.showinfo("Export", "Success, all projects exported successfully!")

        self.open_popup("Export", content)

    def open_settings_popup(self):
        def content(frame):
            ttk.Label(frame, text="Settings", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ctk.CTkButton(frame, text="Reset Credentials", command=reset_credentials, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Delete Account", command=delete_account, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Instructions", command=show_instructions, width=140, height=30, corner_radius=20, fg_color="#805500", hover_color="#664400").pack(pady=(30, 10))
            ctk.CTkButton(frame, text="Submit Bug Ticket", command=show_bug_ticket, width=140, height=30, corner_radius=20, fg_color="#446600", hover_color="#334d00").pack(pady=10)

        def reset_credentials():
            if messagebox.askokcancel("Reset Credentials", "Are you sure you want to reset your credentials?"):
                self.app.show_frame('login')
                popup.destroy()

        def delete_account():
            if messagebox.askokcancel("Delete Account", "Are you sure you want to delete your account? Everything will be lost forever."):
                self.app.user_manager.file_handler.delete_credentials()
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

                ttk.Label(frame, text="Any more questions? Contact email@gmail.com", font=("Helvetica", 10, "italic")).pack(pady=(90, 0))

            self.open_popup("Instructions", content)

        def show_bug_ticket():
            def content(frame):
                ttk.Label(frame, text="Bug Ticket Submission", font=("Helvetica", 16, "bold")).pack(pady=(0, 40))

                ticket_entry = tk.Text(frame, width=80, height=20)
                ticket_entry.pack(pady=(0, 20), padx=20)

                send_button = ctk.CTkButton(frame, text="Submit Ticket", command=lambda: submit_ticket(ticket_entry.get("1.0", tk.END)), width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
                send_button.pack(pady=(0, 30))

            def submit_ticket(ticket):
                subject = 'IDWR Intern Bug Ticket'
                body = ticket
                if subject and body:
                    self.app.user_manager.email_handler.send_email("rohanshahsf@gmail.com", subject, body)
                    self.app.user_manager.email_handler.send_email("lfbianchini@dons.usfca.edu", subject, body)
                    popup.destroy()
                    messagebox.showinfo("Success", "Ticket submitted successfully!")

            self.open_popup("Bug Ticket Submission", content)

        popup = self.open_popup("Change Settings", content)

    def exit_app(self):
        self.app.root.destroy()
