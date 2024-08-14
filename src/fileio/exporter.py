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

    def export_all_projects(self, start_date=None, end_date=None):
        wb = Workbook()
        ws = wb.active
        ws.title = "All Projects and Clients"

        headers = ["Project Name", "Project Description", "Client Name", "Client Description", "Client Company",
                   "LinkedIn", "Email", "Date Created"]
        ws.append(headers)

        projects = ProjectHandler.load_projects_from_directory()

        for project in projects:
            project_date = project.get_date_created()
            print(project_date)
            print(start_date)
            print(end_date)
            if start_date and end_date and not (start_date <= project_date <= end_date):
                continue

            if not project.get_clients():
                ws.append([
                    project.get_name(),
                    project.get_description(),
                    "", "", "", "", "",
                    project.get_date_created_iso()
                ])
            else:
                for client in project.get_clients():
                    if client.get_anonymous():
                        ws.append([
                            project.get_name(),
                            project.get_description(),
                            client.get_name(),
                            client.get_description(),
                            "", "", "",
                            client.get_date_created_iso()
                        ])
                    else:
                        ws.append([
                            project.get_name(),
                            project.get_description(),
                            client.get_name(),
                            client.get_description(),
                            client.get_company(),
                            client.get_linkedin(),
                            client.get_email(),
                            client.get_date_created_iso()
                        ])

        filepath = os.path.join(self.export_dir, f"Full Report, ({start_date.isoformat()} - {end_date.isoformat()}).xlsx")
        wb.save(filepath)
        return filepath

    def export_specific_project(self, project_name, start_date=None, end_date=None):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        project_date = project.get_date_created()
        if start_date and end_date and not (start_date <= project_date <= end_date):
            return None

        wb = Workbook()
        ws = wb.active
        ws.title = f"Project {project.get_name()}"

        headers = ["Client Name", "Client Description", "Client Company", "LinkedIn", "Email", "Date Created"]
        ws.append(headers)

        for client in project.get_clients():
            if client.get_anonymous():
                ws.append([
                    client.get_name(),
                    client.get_description(),
                    "", "", "",
                    client.get_date_created_iso()
                ])
            else:
                ws.append([
                    client.get_name(),
                    client.get_description(),
                    client.get_company(),
                    client.get_linkedin(),
                    client.get_email(),
                    client.get_date_created_iso()
                ])

        filepath = os.path.join(self.export_dir, f"{project.get_name()} Report, ({start_date.isoformat()} - {end_date.isoformat()}).xlsx")
        wb.save(filepath)
        return filepath

    def export_specific_client(self, project_name, client_name, start_date=None, end_date=None):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        project_date = project.get_date_created()
        if start_date and end_date and not (start_date <= project_date <= end_date):
            return None

        client = next((c for c in project.get_clients() if c.get_name() == client_name), None)
        if not client:
            return None

        wb = Workbook()
        ws = wb.active
        ws.title = f"Client {client.get_name()}"

        headers = ["Client Name", "Client Description", "Client Company", "LinkedIn", "Email", "Date Created"]
        ws.append(headers)

        if client.get_anonymous():
            ws.append([
                client.get_name(),
                client.get_description(),
                "", "", "",
                client.get_date_created_iso()
            ])
        else:
            ws.append([
                client.get_name(),
                client.get_description(),
                client.get_company(),
                client.get_linkedin(),
                client.get_email(),
                client.get_date_created_iso()
            ])

        filepath = os.path.join(self.export_dir, f"{client.get_name()} Report, ({start_date.isoformat()} - {end_date.isoformat()}).xlsx")
        wb.save(filepath)
        return filepath


class CSVExporter:
    def __init__(self):
        self.export_dir = 'exports'
        os.makedirs(self.export_dir, exist_ok=True)

    def export_all_projects(self, start_date=None, end_date=None):
        filepath = os.path.join(self.export_dir, f"Full Report, ({start_date.isoformat()} - {end_date.isoformat()}).csv")

        projects = ProjectHandler.load_projects_from_directory()

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(
                ["Project Name", "Project Description", "Client Name", "Client Description", "Client Company",
                 "LinkedIn", "Email", "Date Created"])

            for project in projects:
                project_date = project.get_date_created()
                if start_date and end_date and not (start_date <= project_date <= end_date):
                    continue

                if not project.get_clients():
                    writer.writerow([
                        project.get_name(),
                        project.get_description().replace('\n', ' '),
                        "", "", "", "", "",
                        project.get_date_created_iso()
                    ])
                else:
                    for client in project.get_clients():
                        if client.get_anonymous():
                            writer.writerow([
                                project.get_name(),
                                project.get_description().replace('\n', ' '),
                                client.get_name(),
                                client.get_description().replace('\n', ' '),
                                "", "", "",
                                client.get_date_created_iso()
                            ])
                        else:
                            writer.writerow([
                                project.get_name(),
                                project.get_description().replace('\n', ' '),
                                client.get_name(),
                                client.get_description().replace('\n', ' '),
                                client.get_company(),
                                client.get_linkedin(),
                                client.get_email(),
                                client.get_date_created_iso()
                            ])

        return filepath

    def export_specific_project(self, project_name, start_date=None, end_date=None):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        project_date = project.get_date_created()
        if start_date and end_date and not (start_date <= project_date <= end_date):
            return None

        filepath = os.path.join(self.export_dir, f"{project.get_name()} Report, ({start_date.isoformat()} - {end_date.isoformat()}).csv")

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(
                ["Client Name", "Client Description", "Client Company", "LinkedIn", "Email", "Date Created"])

            for client in project.get_clients():
                if client.get_anonymous():
                    writer.writerow([
                        client.get_name(),
                        client.get_description().replace('\n', ' '),
                        "", "", "",
                        client.get_date_created_iso()
                    ])
                else:
                    writer.writerow([
                        client.get_name(),
                        client.get_description().replace('\n', ' '),
                        client.get_company(),
                        client.get_linkedin(),
                        client.get_email(),
                        client.get_date_created_iso()
                    ])

        return filepath

    def export_specific_client(self, project_name, client_name, start_date=None, end_date=None):
        project = ProjectHandler.load_project(project_name)
        if not project:
            return None

        project_date = project.get_date_created()
        if start_date and end_date and not (start_date <= project_date <= end_date):
            return None

        client = next((c for c in project.get_clients() if c.get_name() == client_name), None)
        if not client:
            return None

        filepath = os.path.join(self.export_dir, f"{client.get_name()} Report, ({start_date.isoformat()} - {end_date.isoformat()}).csv")

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(
                ["Client Name", "Client Description", "Client Company", "LinkedIn", "Email", "Date Created"])

            if client.get_anonymous():
                writer.writerow([
                    client.get_name(),
                    client.get_description().replace('\n', ' '),
                    "", "", "",
                    client.get_date_created_iso()
                ])
            else:
                writer.writerow([
                    client.get_name(),
                    client.get_description().replace('\n', ' '),
                    client.get_company(),
                    client.get_linkedin(),
                    client.get_email(),
                    client.get_date_created_iso()
                ])

        return filepath
