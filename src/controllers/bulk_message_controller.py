import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

selected_clients = []

class BulkMessageController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)

        self.clients = None

        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE)
        self.listbox.pack(pady=(150,0))

        save_btn = ttk.Button(self.frame, text="Save Selections", command=self.save_selections)
        save_btn.pack(pady=10)

        options_frame = ttk.Frame(self.frame)
        options_frame.pack(pady=20)

        self.select_linkedin_btn = ttk.Button(options_frame, text="LinkedIn Messaging", command=self.open_select_linkedin_popup, width=20)
        self.select_linkedin_btn.pack(pady=10)

        self.select_email_btn = ttk.Button(options_frame, text="Email Messaging", command=self.open_select_email_popup, width=20)
        self.select_email_btn.pack(pady=10)

        self.exit_btn = ttk.Button(self.frame, text="Back", command=self.go_to_job, width=10)
        self.exit_btn.pack(side=tk.BOTTOM, pady=(30, 10))

    def update_clients(self):
        if self.app.selected_job:
            self.clients = self.app.selected_job.get_all_client_names()
            self.populate_listbox()

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)  # Clear the listbox
        if self.clients:
            for client in self.clients:
                self.listbox.insert(tk.END, client)

    def save_selections(self):
        global selected_clients
        selected_clients = [self.clients[idx] for idx in self.listbox.curselection()]
        print("Selected clients:", selected_clients)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_clients()

    def hide(self):
        self.frame.pack_forget()

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
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

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

    def open_select_linkedin_popup(self):
        def content(frame):
            ttk.Label(frame, text="LinkedIn", font=("Helvetica", 16, "bold")).pack(pady=10)
            ttk.Label(frame, text="Selected clients:", font=("Helvetica", 12)).pack(pady=10)
            for client in selected_clients:
                ttk.Label(frame, text=client).pack()

            ttk.Label(frame, text="Message Content").pack(pady=(60,0))
            message_content = tk.Text(frame, width=40, height=5)
            message_content.pack(pady=10, padx=20)

            def send_message():
                message = message_content.get("1.0", tk.END).strip()
                for client in selected_clients:
                    if message:
                        self.app.user_manager.linkedin_handler.send_linkedin_message(client, message)
                message_content.delete("1.0", tk.END)

            ttk.Button(frame, text="Send message", command=send_message, width=20).pack(pady=10)

        popup = self.open_popup("LinkedIn", content)

    def open_select_email_popup(self):
        def content(frame):
            ttk.Label(frame, text="Email", font=("Helvetica", 16, "bold")).pack(pady=10)
            ttk.Label(frame, text="Selected clients:", font=("Helvetica", 12)).pack(pady=5)
            for client in selected_clients:
                ttk.Label(frame, text=client).pack()

            ttk.Label(frame, text="Subject:").pack(pady=(60,0))
            subject_entry = ttk.Entry(frame, width=40)
            subject_entry.pack(pady=(0,10))

            ttk.Label(frame, text="Message Body:").pack(pady=(10,5))
            body_text = tk.Text(frame, width=40, height=10)
            body_text.pack(pady=(0,10))

            def send_email():
                subject = subject_entry.get().strip()
                body = body_text.get("1.0", tk.END).strip()
                for client in selected_clients:
                    if subject and body:
                        self.app.user_manager.email_handler.send_email(client, subject, body)
                subject_entry.delete(0, tk.END)
                body_text.delete("1.0", tk.END)

            ttk.Button(frame, text="Send Email", command=send_email, width=20).pack(pady=10)

        popup = self.open_popup("Email", content)

    def go_to_job(self):
        self.app.show_frame('job')
