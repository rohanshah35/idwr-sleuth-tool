import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from src.utils.constants import SUB_FRAME_WIDTH, SUB_FRAME_HEIGHT

selected_clients = []


class BulkMessageController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        self.clients = None
        self.client_vars = []

        self.frame.pack(fill=tk.BOTH, expand=True)

        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(expand=False, pady=(100, 0))

        buttons_frame = ttk.Frame(self.content_frame)
        buttons_frame.pack(pady=(0, 30))

        self.select_linkedin_btn = ctk.CTkButton(buttons_frame, text="LinkedIn Messaging", command=self.open_select_linkedin_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.select_linkedin_btn.pack(side=tk.LEFT, padx=5)

        self.select_email_btn = ctk.CTkButton(buttons_frame, text="Email Messaging", command=self.open_select_email_popup, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.select_email_btn.pack(side=tk.LEFT, padx=5)

        self.checkbox_frame = ttk.Frame(self.content_frame)
        self.checkbox_frame.pack(pady=10)

        # spacer_frame = ttk.Frame(self.frame)
        # spacer_frame.pack(expand=True)

        self.exit_btn = ctk.CTkButton(self.frame, text="Back", command=self.go_to_project, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38")
        self.exit_btn.pack(side=tk.BOTTOM, pady=(30, 20))

    def update_clients(self):
        if self.app.selected_project:
            self.clients = self.app.selected_project.get_all_client_names()
            self.populate_checkboxes()

    def populate_checkboxes(self):
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        self.client_vars = []
        if self.clients:
            for client in self.clients:
                var = tk.BooleanVar()
                checkbox = ctk.CTkCheckBox(self.checkbox_frame,
                                           text=client,
                                           variable=var,
                                           fg_color="#3498db",
                                           hover_color="#2980b9",
                                           text_color="white",
                                           border_color="#2C3E50",
                                           checkmark_color="white")
                checkbox.pack(pady=3)
                self.client_vars.append((client, var))

    def save_selections(self):
        global selected_clients
        selected_clients = [client for client, var in self.client_vars if var.get()]

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_clients()

    def hide(self):
        self.frame.pack_forget()

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

    def open_select_linkedin_popup(self):
        def content(frame):
            ttk.Label(frame, text="LinkedIn", font=("Helvetica", 16, "bold")).pack(pady=10)
            ttk.Label(frame, text="Selected clients:", font=("Helvetica", 12)).pack(pady=10)
            for client in selected_clients:
                ttk.Label(frame, text=client, foreground="white").pack()

            ttk.Label(frame, text="Message Content").pack(pady=(60, 0))
            message_content = tk.Text(frame, width=40, height=5)
            message_content.pack(pady=10, padx=20)

            def send_message():
                message = message_content.get("1.0", tk.END).strip()
                for client in selected_clients:
                    if message:
                        self.app.user_manager.linkedin_handler.send_linkedin_message(client, message)
                message_content.delete("1.0", tk.END)

            ctk.CTkButton(frame, text="Send message", command=send_message, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        self.save_selections()
        popup = self.open_popup("LinkedIn", content)

    def open_select_email_popup(self):
        def content(frame):
            ttk.Label(frame, text="Email", font=("Helvetica", 16, "bold")).pack(pady=10)
            ttk.Label(frame, text="Selected clients:", font=("Helvetica", 12)).pack(pady=5)
            for client in selected_clients:
                ttk.Label(frame, text=client, foreground="white").pack()

            ttk.Label(frame, text="Subject:").pack(pady=(60, 0))
            subject_entry = ttk.Entry(frame, width=40)
            subject_entry.pack(pady=(0, 10))

            ttk.Label(frame, text="Message Body:").pack(pady=(10, 5))
            body_text = tk.Text(frame, width=40, height=10)
            body_text.pack(pady=(0, 10))

            def send_email():
                subject = subject_entry.get().strip()
                body = body_text.get("1.0", tk.END).strip()
                for client in selected_clients:
                    if subject and body:
                        self.app.user_manager.email_handler.send_email(client, subject, body)
                subject_entry.delete(0, tk.END)
                body_text.delete("1.0", tk.END)

            ctk.CTkButton(frame, text="Send Email", command=send_email, width=140, height=30, corner_radius=20, fg_color="#2C3E50", hover_color="#1F2A38").pack(pady=10)

        self.save_selections()
        popup = self.open_popup("Email", content)

    def go_to_project(self):
        self.app.show_frame('project')
