import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import customtkinter as ctk
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

    def open_linkedin_conversation_popup(self):
        def content(frame):
            ttk.Label(frame, text="LinkedIn Conversation", font=("Helvetica", 16, "bold")).pack(pady=10)

            conversation_frame = ttk.Frame(frame, borderwidth=1, relief="solid")
            conversation_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            canvas = tk.Canvas(conversation_frame)
            scrollbar = ttk.Scrollbar(conversation_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            def update_conversation():
                self.app.root.update()

                for widget in scrollable_frame.winfo_children():
                    widget.destroy()

                conversation_text = self.app.user_manager.linkedin_handler.get_conversation_text(self.app.selected_client.linkedin)
                client_name = self.app.selected_client.get_name()

                for message in conversation_text:
                    parts = message.split(': ', 1)
                    if len(parts) == 2:
                        sender, content = parts
                        if sender == client_name:
                            prefix = f"{client_name}: "
                            anchor = "w"
                            side = "left"
                        else:
                            prefix = "You: "
                            anchor = "e"
                            side = "left"

                        message_frame = ttk.Frame(scrollable_frame)
                        message_frame.pack(fill="x", pady=5, padx=10)

                        ttk.Label(message_frame, text=prefix, anchor=anchor, foreground='#555555').pack(side=side)
                        ttk.Label(message_frame, text=content, anchor=anchor).pack(side=side)
                    else:
                        ttk.Label(scrollable_frame, text=message, anchor="w").pack(pady=5, padx=10, fill="x")

                    separator_frame = ttk.Frame(scrollable_frame)
                    separator_frame.pack(fill="x", pady=5, padx=10)
                    ttk.Separator(separator_frame, orient='horizontal').pack(fill='x')

                scrollable_frame.update_idletasks()
                canvas.yview_moveto(1.0)

            self.app.root.after(100, update_conversation)

            input_frame = ttk.Frame(frame)
            input_frame.pack(fill=tk.X, padx=20, pady=10)

            message_entry = ttk.Entry(input_frame, width=50)
            message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

            def send_message():
                message = message_entry.get()
                if message:
                    self.app.user_manager.linkedin_handler.send_linkedin_message(self.app.selected_client.linkedin, message)
                    message_entry.delete(0, tk.END)
                    update_conversation()

            send_button = ctk.CTkButton(input_frame, text="Send", command=send_message, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
            send_button.pack(side=tk.RIGHT)

        popup = self.open_popup("LinkedIn Conversation", content)

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
