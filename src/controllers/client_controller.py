import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import customtkinter as ctk

from src.fileio.file_handler import ProjectHandler
from src.utils.constants import SUB_FRAME_WIDTH, SUB_FRAME_HEIGHT

from src.fileio.exporter import ExcelExporter, CSVExporter


class ClientController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        options_frame = ttk.Frame(self.frame)
        options_frame.pack(expand=True)

        self.project_label = ttk.Label(options_frame, text="", font=("Helvetica", 18, "bold"))
        self.project_label.pack(pady=(0, 30))

        self.edit_client_btn = ctk.CTkButton(
            options_frame,
            text="Edit Client",
            command=self.open_edit_client_popup,
            width=200,
            height=40,
            corner_radius=20,
            fg_color="#2C3E50",
            hover_color="#1F2A38"
        )
        self.edit_client_btn.pack(pady=(10, 30))

        self.linkedin_conversation_btn = ctk.CTkButton(options_frame, text="LinkedIn Conversation", command=self.open_linkedin_conversation_popup, width=200, height=40, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.linkedin_conversation_btn.pack(pady=10)

        self.email_conversation_btn = ctk.CTkButton(options_frame, text="Email Conversation", command=self.open_email_conversation_popup, width=200, height=40, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.email_conversation_btn.pack(pady=10)

        self.export_btn = ctk.CTkButton(options_frame, text="Export", command=self.open_export_popup, width=200, height=40, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.export_btn.pack(pady=10)

        self.exit_btn = ctk.CTkButton(options_frame, text="Back", command=self.go_to_project, width=200, height=40, corner_radius=20, fg_color="#CC0000", hover_color="#990000")
        self.exit_btn.pack(pady=(30, 10))

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_client()

    def hide(self):
        self.frame.pack_forget()

    def update_client(self):
        self.project_label.config(text=self.app.selected_client.name)

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
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

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

    def open_edit_client_popup(self):
        def content(frame):
            ttk.Label(frame, text="Edit Client", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ttk.Label(frame, text="Client Name:").pack(pady=10)
            client_name_entry = ttk.Entry(frame, width=40)
            client_name_entry.insert(0, self.app.selected_client.get_name())
            client_name_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Description:").pack(pady=10)
            client_desc_entry = tk.Text(frame, width=40, height=5)
            client_desc_entry.insert("1.0", self.app.selected_client.get_description())
            client_desc_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Company:").pack(pady=10)
            client_company_entry = ttk.Entry(frame, width=40)
            client_company_entry.insert(0, self.app.selected_client.get_company())
            client_company_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client LinkedIn URL:").pack(pady=10)
            client_linkedin_entry = ttk.Entry(frame, width=40)
            client_linkedin_entry.insert(0, self.app.selected_client.get_linkedin())
            client_linkedin_entry.pack(pady=(0, 10), padx=20)

            ttk.Label(frame, text="Client Email:").pack(pady=10)
            client_email_entry = ttk.Entry(frame, width=40)
            client_email_entry.insert(0, self.app.selected_client.get_email())
            client_email_entry.pack(pady=(0, 10), padx=20)

            edit_button = ctk.CTkButton(
                frame,
                text="Save Client",
                command=lambda: edit_client(
                    client_name_entry.get(),
                    client_desc_entry.get("1.0", tk.END).strip(),
                    client_company_entry.get(),
                    client_linkedin_entry.get(),
                    client_email_entry.get()
                ),
                width=140,
                height=30,
                corner_radius=20,
                fg_color="#2C3E50",
                hover_color="#1F2A38"
            )
            edit_button.pack(pady=(20, 0))

        def edit_client(client_name, client_description, client_company, client_linkedin, client_email):
            old_name = self.app.selected_client.get_name()

            self.app.selected_client.set_name(client_name)
            self.app.selected_client.set_description(client_description)
            self.app.selected_client.set_company(client_company)
            self.app.selected_client.set_linkedin(client_linkedin)
            self.app.selected_client.set_email(client_email)

            self.app.selected_project.update_client(old_name, self.app.selected_client)

            project_manager = ProjectHandler(self.app.selected_project)
            project_manager.write_project()

            self.update_client()

            popup.destroy()
            messagebox.showinfo("Success", f"Client '{client_name}' edited successfully!")

        popup = self.open_popup("Edit Client", content)

    def open_linkedin_conversation_popup(self):
        self.app.user_manager.linkedin_handler.open_linkedin_conversation_visible(self.app.selected_client)

    def open_email_conversation_popup(self):
        def content(frame):
            ttk.Label(frame, text="Email Conversation", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

            ttk.Label(frame, text="Subject:").pack(anchor="w", padx=20)
            subject_entry = ttk.Entry(frame, width=60)
            subject_entry.pack(pady=(0, 10), padx=20, fill="x")

            ttk.Label(frame, text="Body:").pack(anchor="w", padx=20)
            body_text = tk.Text(frame, width=60, height=10)
            body_text.pack(pady=(0, 20), padx=20, fill="both", expand=True)

            def send_email():
                subject = subject_entry.get()
                body = body_text.get("1.0", tk.END).strip()
                if subject and body:
                    self.app.user_manager.email_handler.send_email(self.app.selected_client.email, subject, body)
                    messagebox.showinfo("Success", "Email sent successfully!")
                    subject_entry.delete(0, tk.END)
                    body_text.delete("1.0", tk.END)
                else:
                    messagebox.showerror("Error", "Please enter both subject and body.")

            send_button = ctk.CTkButton(frame, text="Send Email", command=send_email, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
            send_button.pack(pady=20)

        popup = self.open_popup("Email Conversation", content)

    def open_export_popup(self):
        client_name = self.app.selected_client.get_name()

        def content(frame):
            ttk.Label(frame, text="Export", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

            ctk.CTkButton(frame, text="Export Client (XLS)", command=export_xls, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)
            ctk.CTkButton(frame, text="Export Client (CSV)", command=export_csv, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        def export_xls():
            exporter = ExcelExporter()
            exporter.export_specific_client(self.app.selected_project.get_name(), self.app.selected_client.get_name())
            messagebox.showinfo("Export", f"Success, {client_name} exported successfully!")

        def export_csv():
            exporter = CSVExporter()
            exporter.export_specific_client(self.app.selected_project.get_name(), self.app.selected_client.get_name())
            messagebox.showinfo("Export", f"Success, {client_name} exported successfully!")

        self.open_popup("Export", content)

    def go_to_project(self):
        self.app.show_frame('project')
