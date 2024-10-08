# Handles login menu within GUI

import threading
import tkinter as tk
import ttkbootstrap as ttk
from customtkinter import CTkButton
from ttkbootstrap.constants import *

from src.auth.email_handler import EmailHandler
from src.auth.linkedin_handler import LinkedInHandler
from src.utils.utils import email_validator


class LoginController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.center_frame = ttk.Frame(self.frame)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        title_label = ttk.Label(self.center_frame, text="IDWR Office", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(0, 20))

        self.email_entry = ttk.Entry(self.center_frame, width=40)
        self.email_entry.insert(0, "Email")
        self.email_entry.pack(pady=10)
        self.email_entry.bind("<FocusIn>", lambda e: self.on_entry_click(self.email_entry, "Email"))
        self.email_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.email_entry, "Email"))

        self.email_pass_entry = ttk.Entry(self.center_frame, width=40, show="")
        self.email_pass_entry.insert(0, "Email provider password")
        self.email_pass_entry.pack(pady=10)
        self.email_pass_entry.bind("<FocusIn>",
                                   lambda e: self.on_entry_click(self.email_pass_entry, "Email provider password"))
        self.email_pass_entry.bind("<FocusOut>",
                                   lambda e: self.on_focus_out(self.email_pass_entry, "Email provider password"))

        self.linkedin_email_entry = ttk.Entry(self.center_frame, width=40)
        self.linkedin_email_entry.insert(0, "LinkedIn email")
        self.linkedin_email_entry.pack(pady=10)
        self.linkedin_email_entry.bind("<FocusIn>",
                                       lambda e: self.on_entry_click(self.linkedin_email_entry, "LinkedIn email"))
        self.linkedin_email_entry.bind("<FocusOut>",
                                       lambda e: self.on_focus_out(self.linkedin_email_entry, "LinkedIn email"))

        self.linkedin_pass_entry = ttk.Entry(self.center_frame, width=40, show="")
        self.linkedin_pass_entry.insert(0, "LinkedIn password")
        self.linkedin_pass_entry.pack(pady=10)
        self.linkedin_pass_entry.bind("<FocusIn>",
                                      lambda e: self.on_entry_click(self.linkedin_pass_entry, "LinkedIn password"))
        self.linkedin_pass_entry.bind("<FocusOut>",
                                      lambda e: self.on_focus_out(self.linkedin_pass_entry, "LinkedIn password"))

        login_button = CTkButton(self.center_frame, text="Login", command=self.login, corner_radius=20, width=80,
                                 fg_color="#2C3E50", hover_color="#1F2A38")
        login_button.pack(pady=(20, 0))

        self.error_label = ttk.Label(self.center_frame, text="", foreground="red")
        self.error_label.pack(pady=(20, 0))

    def on_entry_click(self, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, "end")
            if "password" in default_text.lower():
                entry.config(show="•")

    def on_focus_out(self, entry, default_text):
        if entry.get() == "":
            entry.insert(0, default_text)
            if "password" in default_text.lower():
                entry.config(show="")

    def clear_entries(self):
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, "Email")
        self.email_pass_entry.delete(0, "end")
        self.email_pass_entry.insert(0, "Email provider password")
        self.email_pass_entry.config(show="")
        self.linkedin_email_entry.delete(0, "end")
        self.linkedin_email_entry.insert(0, "LinkedIn email")
        self.linkedin_pass_entry.delete(0, "end")
        self.linkedin_pass_entry.insert(0, "LinkedIn password")
        self.linkedin_pass_entry.config(show="")
        self.error_label.config(text="")

    def login(self):
        self.error_label.config(text="")
        email = self.email_entry.get()
        email_password = self.email_pass_entry.get()
        linkedin_email = self.linkedin_email_entry.get()
        linkedin_password = self.linkedin_pass_entry.get()

        if email_validator(email) and email_validator(linkedin_email):
            self.app.show_frame('loading')

            threading.Thread(target=self.perform_login_thread,
                             args=(email, email_password, linkedin_email, linkedin_password),
                             daemon=True).start()
        else:
            self.clear_entries()
            self.error_label.config(text="Invalid email format. Please try again.")

    def perform_login_thread(self, email, email_password, linkedin_email, linkedin_password):
        try:
            self.app.user_manager.set_linkedin_handler(LinkedInHandler(linkedin_email, linkedin_password))
            self.app.user_manager.set_email_handler(EmailHandler(email, email_password))

            self.app.user_manager.get_linkedin_handler().login_to_linkedin_visible_then_headless()
            linkedin_cookies = self.app.user_manager.get_linkedin_handler().get_cookies()
            self.app.user_manager.get_email_handler().initialize_imap()
            self.app.user_manager.get_email_handler().initialize_smtp()

            self.app.user_manager.set_user_data({
                'linkedin_email': linkedin_email,
                'linkedin_password': linkedin_password,
                'email': email,
                'email_password': email_password,
                'linkedin_cookies': linkedin_cookies
            })

            self.app.user_manager.save_user_data()
            self.app.show_frame('home')
        except Exception as e:
            self.app.show_frame('login')
            self.clear_entries()
            self.error_label.config(text="Login unsuccessful. Please try again.")

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()
