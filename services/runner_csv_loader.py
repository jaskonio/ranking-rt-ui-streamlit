import csv
import json
from typing import List
from services.league_services import LeagueServices
from services.person_services import PersonServices
from services.races_services import RacesServices

class PersonFile():
    def __init__(self, first_name: str = '', last_name:str = '', dorsal: int = 0, gender:str = ''
                    ,league_name: str = '', league_id: str = ''):
        self.first_name = first_name
        self.last_name = last_name
        self.dorsal = 0 if dorsal == "CaC" else dorsal
        self.gender = gender
        self.league_name = league_name
        self.league_id = league_id

class Person():
    def __init__(self, id:str='', first_name: str = '', last_name:str = '', nationality: str = '',
                    gender: str = '', photo:str = '', photo_url: str = ''):
        self.id = str(id)
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.photo = photo
        self.photo_url = photo_url

class Runner(Person):
    def __init__(self, id:str='', first_name: str = '', last_name:str = '', nationality: str = '',
                    gender: str = '', photo:str = '', photo_url: str = '', dorsal:int=0, club:str='redolat team',category:str=''):
        super().__init__(id, first_name, last_name, nationality, gender, photo, photo_url)
        self.dorsal = dorsal
        self.club = club
        self.category = category

class RunnerCSV_Loader():
    def __init__(self, race_service:RacesServices, person_service:PersonServices, league_service:LeagueServices) -> None:
        self.race_service:RacesServices = race_service
        self.person_service:PersonServices = person_service
        self.league_service:LeagueServices = league_service
        self.all_leagues = self.league_service.get_all()

    def upload_file(self, csv_content):
        reader = list(csv.reader(csv_content, delimiter=';',))
        persons_file:List[PersonFile] = [PersonFile(first_name=row[1], last_name=row[2], dorsal=row[0], league_name=row[3]) for row in reader]

        league_names = self.league_service.get_all_names()
        all_person_db = self.person_service.get_all()
        all_person_db = [Runner(**item) for item in all_person_db]

        persons_with_invalid_league_name = []

        persons_file_filtered:List[PersonFile] = []
        for person_file in persons_file:
            if person_file.league_name not in league_names or person_file.league_name == '':
                persons_with_invalid_league_name.append(person_file.first_name)
                continue

            persons_file_filtered.append(person_file)

        dict_league_name_with_persons = {}

        persons_duplicated = []
        persons_name_not_found_in_db = []

        for person_file in persons_file_filtered:
            persons = list(filter(lambda item: item.first_name + item.last_name == person_file.first_name + person_file.last_name, all_person_db))
            if len(persons) == 0 :
                persons_name_not_found_in_db.append(person_file.first_name)
                continue

            if len(persons) >= 2:
                persons_duplicated.append(person_file.first_name)
                continue

            if person_file.league_name not in dict_league_name_with_persons.keys():
                dict_league_name_with_persons[person_file.league_name] = []

            person = persons[0]
            person.dorsal = person_file.dorsal
            dict_league_name_with_persons[person_file.league_name].append(person)

        for key, values in dict_league_name_with_persons.items():
            league = list(filter(lambda league: league['name']== key, self.all_leagues))[0]
            values = [value.__dict__ for value in values]
            self.league_service.add_runners_by_league_id(league['id'], values)

        print("Hay persona que no tienen liga: ")
        print(persons_with_invalid_league_name)
        print("Hay persona duplicadas: ")
        print(persons_duplicated)
        print("Hay persona que no estan en la base de datos: ")
        print(persons_name_not_found_in_db)

        return True
