# Main controller for application
import concurrent.futures
import time
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

        self.entire_client_list = self.get_all_clients_from_projects()
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
        if self.user_manager.get_user_data():
            self.show_frame('loading')
            self.root.after(100, self.validate_credentials)
        else:
            self.show_frame('login')

    def update_project_list(self):
        self.project_list = ProjectHandler.load_projects_from_directory()

    def update_entire_client_list(self):
        self.entire_client_list = self.get_all_clients_from_projects()

    def get_all_clients_from_projects(self):
        all_clients = []

        for project in self.project_list:
            project_clients = project.get_clients()
            all_clients.extend(project_clients)

        return all_clients

    def validate_credentials(self):
        start_total = time.time()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            cookies_future = executor.submit(self.check_linkedin_cookies)
            email_future = executor.submit(self.validate_email)

            cookies_valid = cookies_future.result()
            email_valid = email_future.result()

        end_total = time.time()
        total_time = end_total - start_total

        print(f"Total time: {total_time:.4f} seconds")

        self.controllers['loading'].hide()

        if cookies_valid and email_valid:
            self.show_frame('home')
        else:
            self.show_frame('login')

    # def validate_credentials(self):
    #     start_total = time.time()
    #
    #     start_cookies = time.time()
    #     cookies_valid = self.check_linkedin_cookies()
    #     end_cookies = time.time()
    #     cookies_time = end_cookies - start_cookies
    #
    #     start_email = time.time()
    #     email_valid = self.validate_email()
    #     end_email = time.time()
    #     email_time = end_email - start_email
    #
    #     end_total = time.time()
    #     total_time = end_total - start_total
    #
    #     print(f"Time to check LinkedIn cookies: {cookies_time:.4f} seconds")
    #     print(f"Time to validate email: {email_time:.4f} seconds")
    #     print(f"Total time: {total_time:.4f} seconds")
    #
    #     self.controllers['loading'].hide()
    #
    #     if cookies_valid and email_valid:
    #         self.show_frame('home')
    #     else:
    #         self.show_frame('login')

    def check_linkedin_cookies(self):
        if not self.user_manager.get_linkedin_handler():
            self.user_manager.set_linkedin_handler(LinkedInHandler(
                self.user_manager.get_user_data()['linkedin_email'],
                self.user_manager.get_user_data()['linkedin_password']
            ))

        cookies = self.user_manager.get_user_data().get('linkedin_cookies')
        if cookies and self.user_manager.get_linkedin_handler().login_with_cookies(cookies):
            return True
        else:
            return self.user_manager.get_linkedin_handler().login_to_linkedin()

    def validate_email(self):
        if not self.user_manager.get_email_handler():
            self.user_manager.set_email_handler(EmailHandler(
                self.user_manager.get_user_data()['email'],
                self.user_manager.get_user_data()['email_password']
            ))

        try:
            self.user_manager.get_email_handler().initialize_smtp()
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


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
