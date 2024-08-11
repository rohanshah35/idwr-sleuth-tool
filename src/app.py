# Main controller for application
import tkinter as tk
import ttkbootstrap as ttk

from src.auth.email_handler import EmailHandler
from src.auth.linkedin_handler import LinkedInHandler
from src.controllers.loading_screen import LoadingScreenController
from src.controllers.login_controller import LoginController
from src.controllers.home_controller import HomeController
from src.controllers.project_controller import ProjectController
from src.controllers.client_controller import ClientController
from src.controllers.bulk_message_controller import BulkMessageController
from src.fileio.file_handler import ProjectHandler
from src.utils.constants import FRAME_HEIGHT, FRAME_WIDTH

from src.structures.user import UserManager


class App:
    def __init__(self):
        self.root = ttk.Window(title='IDWR Intern V1.0', themename='darkly', size=(FRAME_WIDTH, FRAME_HEIGHT),
                               resizable=(False, False))

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.user_manager = UserManager()

        self.project_list = ProjectHandler.load_projects_from_directory()
        self.selected_project = None

        self.client_list = None
        self.selected_client = None

        self.controllers = {
            'login': LoginController(self),
            'home': HomeController(self),
            'project': ProjectController(self),
            'client': ClientController(self),
            'loading': LoadingScreenController(self),
            'bulk': BulkMessageController(self),
        }
        if self.user_manager.user_data:
            self.validate_credentials()
        else:
            self.show_frame('login')

    def validate_credentials(self):
        if True:
            if True:
                self.show_frame('home')
            else:
                self.show_frame('login')
        else:
            self.show_frame('login')

    def check_linkedin_cookies(self):
        if not self.user_manager.linkedin_handler:
            self.user_manager.linkedin_handler = LinkedInHandler(
                self.user_manager.user_data['linkedin_email'],
                self.user_manager.user_data['linkedin_password']
            )

        cookies = self.user_manager.user_data.get('linkedin_cookies')
        if cookies and self.user_manager.linkedin_handler.login_with_cookies(cookies):
            return True
        else:
            return self.user_manager.linkedin_handler.login_to_linkedin()

    def validate_email(self):
        if not self.user_manager.email_handler:
            self.user_manager.email_handler = EmailHandler(
                self.user_manager.user_data['email'],
                self.user_manager.user_data['email_password']
            )

        try:
            self.user_manager.email_handler.initialize_smtp()
            self.user_manager.email_handler.initialize_imap()
            return True
        except Exception as e:
            print(f"An error occurred while validating email: {str(e)}")
            return False

    def show_frame(self, controller_name):
        for controller in self.controllers.values():
            if hasattr(controller, 'hide'):
                controller.hide()

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
