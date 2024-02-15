import csv
from typing import List
from models.person_models import PersonFile


class CSV_reader():
    @staticmethod
    def reader(data, delimiter=";", exclude_header=False):
        reader = csv.reader(data, delimiter=delimiter)
        if exclude_header:
            next(reader)

        reader = list(reader)
        return reader

    @staticmethod
    def convertCsvToPersonFile(data, delimiter=";", exclude_header=False):
        rows = CSV_reader().reader(data, delimiter=delimiter, exclude_header=exclude_header)
        persons_file:List[PersonFile] = [PersonFile(first_name=row[1], last_name=row[2], dorsal=row[0], league_name=row[3]) for row in rows]
        return persons_file
