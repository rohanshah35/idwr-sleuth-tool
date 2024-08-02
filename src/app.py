# Main controller for application
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.controllers.login_controller import LoginController
from src.controllers.home_controller import HomeController
from src.controllers.job_controller import JobController
from src.controllers.client_controller import ClientController
from src.fileio.file_handler import JobHandler

from src.structures.user import UserManager


class App:
    def __init__(self):
        self.root = ttk.Window(title='IDWR Intern V1.0', themename='darkly', size=(1440, 900), resizable=(False, False))

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.user_manager = UserManager()

        self.email = ""
        self.email_password = ""
        self.linkedin_password = ""

        self.linkedin_handler = None
        self.email_handler = None

        self.job_list = JobHandler.load_jobs_from_directory()
        self.selected_job = None

        self.client_list = None
        self.selected_client = None

        self.controllers = {
            'login': LoginController(self),
            'home': HomeController(self),
            'job': JobController(self),
            'client': ClientController(self)
        }

        if self.user_manager.user_data:
            self.show_frame('home')
            # self.user_manager.linkedin_handler.login_to_linkedin_headless()
            # self.user_manager.email_handler.initialize_imap()
            # self.user_manager.email_handler.initialize_smtp()
        else:
            self.show_frame('login')

    def show_frame(self, controller_name):
        # Hide all frames
        for controller in self.controllers.values():
            if hasattr(controller, 'hide'):
                controller.hide()

        # Show the requested frame
        frame = self.controllers[controller_name]
        if hasattr(frame, 'show'):
            frame.show()
        else:
            frame.frame.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
