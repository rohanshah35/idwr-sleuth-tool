import os
import csv
from openpyxl import Workbook
from src.fileio.file_handler import ProjectHandler
from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d')


class ExcelExporter:
    def __init__(self):
        self.export_dir = 'exports'
        os.makedirs(self.export_dir, exist_ok=True)

    def export_all_projects(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "All Projects and Clients"

        headers = ["Project Name", "Project Description", "Client Name", "Client Description", "Client Company", "LinkedIn", "Email"]
        ws.append(headers)

        projects = ProjectHandler.load_projects_from_directory()

        for project in projects:
            if not project.get_clients():
                ws.append([
                    project.get_name(),
                    project.get_description(),
                ])
            else:
                for client in project.get_clients():
                    ws.append([
                        project.get_name(),
                        project.get_description(),
                        client.get_name(),
                        client.description,
                        client.company,
                        client.linkedin,
                        client.get_email()
                    ])

        filepath = os.path.join(self.export_dir, f"Full Report, ({date}).xlsx")
        wb.save(filepath)
        return filepath

    def export_specific_project(self, project_name):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        wb = Workbook()
        ws = wb.active
        ws.title = f"Project {project.get_name()}"

        headers = ["Client Name", "Client Description", "Client Company", "LinkedIn", "Email"]
        ws.append(headers)

        for client in project.get_clients():
            ws.append([
                client.get_name(),
                client.description,
                client.company,
                client.linkedin,
                client.get_email()
            ])

        filepath = os.path.join(self.export_dir, f"{project.get_name()} Report, ({date}).xlsx")
        wb.save(filepath)
        return filepath

    def export_specific_client(self, project_name, client_name):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        client = next((c for c in project.get_clients() if c.get_name() == client_name), None)
        if not client:
            return None

        wb = Workbook()
        ws = wb.active
        ws.title = f"Client {client.get_name()}"

        headers = ["Client Name", "Client Description", "Client Company", "LinkedIn", "Email"]
        ws.append(headers)

        ws.append([
            client.get_name(),
            client.description,
            client.company,
            client.linkedin,
            client.get_email()
        ])

        filepath = os.path.join(self.export_dir, f"{client.get_name()} Report, ({date}).xlsx")
        wb.save(filepath)
        return filepath


class CSVExporter:
    def __init__(self):
        self.export_dir = 'exports'
        os.makedirs(self.export_dir, exist_ok=True)

    def export_all_projects(self):
        filepath = os.path.join(self.export_dir, f"Full Report, ({date}).csv")

        projects = ProjectHandler.load_projects_from_directory()

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(["Project Name", "Project Description", "Client Name", "Client Description", "Client Company", "LinkedIn", "Email"])

            for project in projects:
                if not project.get_clients():
                    writer.writerow([
                        project.get_name(),
                        project.get_description().replace('\n', ' '),
                        "", "", "", ""
                    ])
                else:
                    for client in project.get_clients():
                        writer.writerow([
                            project.get_name(),
                            project.get_description().replace('\n', ' '),
                            client.get_name(),
                            client.description.replace('\n', ' '),
                            client.company,
                            client.linkedin,
                            client.get_email()
                        ])

        return filepath

    def export_specific_project(self, project_name):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        filepath = os.path.join(self.export_dir, f"{project.get_name()} Report, ({date}).csv")

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(["Client Name", "Client Description", "Client Company", "LinkedIn", "Email"])

            for client in project.get_clients():
                writer.writerow([
                    client.get_name(),
                    client.description.replace('\n', ' '),
                    client.company,
                    client.linkedin,
                    client.get_email()
                ])

        return filepath

    def export_specific_client(self, project_name, client_name):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        client = next((c for c in project.get_clients() if c.get_name() == client_name), None)
        if not client:
            return None

        filepath = os.path.join(self.export_dir, f"{client.get_name()} Report, ({date}).csv")

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(["Client Name", "Client Description", "Client Company", "LinkedIn", "Email"])
            writer.writerow([
                client.get_name(),
                client.description.replace('\n', ' '),
                client.company,
                client.linkedin,
                client.get_email()
            ])

        return filepath