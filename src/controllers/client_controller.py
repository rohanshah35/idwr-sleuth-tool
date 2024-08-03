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
        popup.resizable(False, False)

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

            conversation_text = self.app.linkedin_handler.get_conversation_text(self.app.selected_client.linkedin)

            for message in conversation_text:
                parts = message.split(': ', 1)
                if len(parts) == 2:
                    sender, content = parts
                    if sender == "You":
                        ttk.Label(scrollable_frame, text=content, anchor="e", wraplength=300).pack(pady=5, padx=(50, 10), fill="x")
                    else:
                        ttk.Label(scrollable_frame, text=content, anchor="w", wraplength=300).pack(pady=5, padx=(10, 50), fill="x")
                else:
                    ttk.Label(scrollable_frame, text=message, anchor="w", wraplength=300).pack(pady=5, padx=10, fill="x")

            input_frame = ttk.Frame(frame)
            input_frame.pack(fill=tk.X, padx=20, pady=10)

            message_entry = ttk.Entry(input_frame, width=50)
            message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

            def send_message():
                message = message_entry.get()
                if message:
                    self.app.linkedin_handler.send_linkedin_message(self.app.selected_client.linkedin, message)
                    message_entry.delete(0, tk.END)

            send_button = ttk.Button(input_frame, text="Send", command=send_message)
            send_button.pack(side=tk.RIGHT)

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
            messagebox.showinfo("Export", f"Success, {client_name} exported successfully!")

        def export_csv():
            exporter = CSVExporter()
            exporter.export_specific_client(self.app.selected_job.get_name(), self.app.selected_client.get_name())
            messagebox.showinfo("Export", f"Success, {client_name} exported successfully!")

        self.open_popup("Export", content)

    def go_to_job(self):
        self.app.show_frame('job')
