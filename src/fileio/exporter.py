import os
import csv
from openpyxl import Workbook
from src.fileio.file_handler import JobHandler


class ExcelExporter:
    def __init__(self):
        self.export_dir = 'exports'
        os.makedirs(self.export_dir, exist_ok=True)

    def export_all_jobs(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "All Jobs and Clients"

        headers = ["Job Name", "Job Description", "Client Name", "Client Description", "LinkedIn", "Email"]
        ws.append(headers)

        jobs = JobHandler.load_jobs_from_directory()

        for job in jobs:
            for client in job.get_clients():
                ws.append([
                    job.get_name(),
                    job.get_description(),
                    client.get_name(),
                    client.description,
                    client.linkedin,
                    client.get_email()
                ])

        filepath = os.path.join(self.export_dir, "all_jobs_and_clients.xlsx")
        wb.save(filepath)
        return filepath

    def export_specific_job(self, job_name):
        job = JobHandler.load_job(job_name)
        if not job:
            return None

        wb = Workbook()
        ws = wb.active
        ws.title = f"Job {job.get_name()}"

        headers = ["Client Name", "Client Description", "LinkedIn", "Email"]
        ws.append(headers)

        for client in job.get_clients():
            ws.append([
                client.get_name(),
                client.description,
                client.linkedin,
                client.get_email()
            ])

        filepath = os.path.join(self.export_dir, f"{job.get_name()}_clients.xlsx")
        wb.save(filepath)
        return filepath

    def export_specific_client(self, job_name, client_name):
        job = JobHandler.load_job(job_name)
        if not job:
            return None

        client = next((c for c in job.get_clients() if c.get_name() == client_name), None)
        if not client:
            return None

        wb = Workbook()
        ws = wb.active
        ws.title = f"Client {client.get_name()}"

        headers = ["Client Name", "Client Description", "LinkedIn", "Email"]
        ws.append(headers)

        ws.append([
            client.get_name(),
            client.description,
            client.linkedin,
            client.get_email()
        ])

        filepath = os.path.join(self.export_dir, f"{job.get_name()}_{client.get_name()}.xlsx")
        wb.save(filepath)
        return filepath


class CSVExporter:
    def __init__(self):
        self.export_dir = 'exports'
        os.makedirs(self.export_dir, exist_ok=True)

    def export_all_jobs(self):
        filepath = os.path.join(self.export_dir, "all_jobs_and_clients.csv")

        jobs = JobHandler.load_jobs_from_directory()

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Job Name", "Job Description", "Client Name", "Client Description", "LinkedIn", "Email"])

            for job in jobs:
                for client in job.get_clients():
                    writer.writerow([
                        job.get_name(),
                        job.get_description(),
                        client.get_name(),
                        client.description,
                        client.linkedin,
                        client.get_email()
                    ])

        return filepath

    def export_specific_job(self, job_name):
        job = JobHandler.load_job(job_name)
        if not job:
            return None

        filepath = os.path.join(self.export_dir, f"{job.get_name()}_clients.csv")

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Client Name", "Client Description", "LinkedIn", "Email"])

            for client in job.get_clients():
                writer.writerow([
                    client.get_name(),
                    client.description,
                    client.linkedin,
                    client.get_email()
                ])

        return filepath

    def export_specific_client(self, job_name, client_name):
        job = JobHandler.load_job(job_name)
        if not job:
            return None

        client = next((c for c in job.get_clients() if c.get_name() == client_name), None)
        if not client:
            return None

        filepath = os.path.join(self.export_dir, f"{job.get_name()}_{client.get_name()}.csv")

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Client Name", "Client Description", "LinkedIn", "Email"])
            writer.writerow([
                client.get_name(),
                client.description,
                client.linkedin,
                client.get_email()
            ])

        return filepath