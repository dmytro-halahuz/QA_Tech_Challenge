import csv
import io
import os
import allure

def get_env_var(name, hidden=False):
    var = os.environ[name]
    if hidden:
        allure.dynamic.parameter(name, var, mode=allure.parameter_mode.MASKED)
    else:
        allure.dynamic.parameter(name, var)

    return var

class TempCSVFile:
    def __init__(self, name):
        self.name = name
        self.buffer = io.StringIO()
        self.writer = csv.writer(self.buffer)

    def writerow(self, row):
        self.writer.writerow(row)

    def writerows(self, rows):
        self.writer.writerows(rows)

    def attach_to_report(self):
        allure.attach(
            self.buffer.getvalue(),
            name=self.name,
            attachment_type="text/csv",
            extension="csv"
        )