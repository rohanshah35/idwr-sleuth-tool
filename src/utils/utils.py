# General utility

import re
import tkinter as tk
from datetime import date
from tkinter import ttk


# Validates email credentials
def email_validator(input_string):
    match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', input_string)

    if match is None:
        return False
    return True


class DateEntry(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.year = ttk.Combobox(self, width=5, values=[str(year) for year in range(2000, 2101)])
        self.month = ttk.Combobox(self, width=3, values=[f"{month:02d}" for month in range(1, 13)])
        self.day = ttk.Combobox(self, width=3, values=[f"{day:02d}" for day in range(1, 32)])

        self.year.pack(side=tk.LEFT, padx=2)
        self.month.pack(side=tk.LEFT, padx=2)
        self.day.pack(side=tk.LEFT, padx=2)

        today = date.today()
        self.year.set(str(today.year))
        self.month.set(f"{today.month:02d}")
        self.day.set(f"{today.day:02d}")

    def get_date(self):
        return date(int(self.year.get()), int(self.month.get()), int(self.day.get()))
