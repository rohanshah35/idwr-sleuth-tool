# Main controller for application
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.auth.email_handler import EmailHandler
from src.auth.linkedin_handler import LinkedInHandler
from src.controllers.loading_screen import LoadingScreenController
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

        self.job_list = JobHandler.load_jobs_from_directory()
        self.selected_job = None

        self.client_list = None
        self.selected_client = None

        self.controllers = {
            'login': LoginController(self),
            'home': HomeController(self),
            'job': JobController(self),
            'client': ClientController(self),
            'loading': LoadingScreenController(self)
        }

        if self.user_manager.user_data:
            # self.user_manager.load_handlers()
            # self.user_manager.linkedin_handler.login_to_linkedin_headless()
            # self.user_manager.email_handler.initialize_smtp()
            # self.user_manager.email_handler.initialize_imap()
            self.show_frame('home')
        else:
            self.show_frame('login')

    def show_frame(self, controller_name):
        for controller in self.controllers.values():
            if hasattr(controller, 'hide'):
                controller.hide()

        frame = self.controllers[controller_name]
        self.current_frame = controller_name
        if hasattr(frame, 'show'):
            frame.show()
        else:
            frame.frame.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
