from typing import List
from models.person_models import PersonFile, Runner
from services.league_services import LeagueServices
from services.person_services import PersonServices
from services.races_services import RacesServices
from services.notification_service import NotificationServices

class RunnerCSV_Loader():
    def __init__(self, race_service:RacesServices, person_service:PersonServices, league_service:LeagueServices, notification_services:NotificationServices) -> None:
        self.race_service:RacesServices = race_service
        self.person_service:PersonServices = person_service
        self.league_service:LeagueServices = league_service
        self.notification_services:NotificationServices = notification_services

        self.all_leagues = self.league_service.get_all()

    def upload_file(self, persons_file):
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

        if len(persons_with_invalid_league_name) != 0:
            self.notification_services.show_warnning(f"Hay persona que no tienen liga: {str(persons_with_invalid_league_name)}")

        if len(persons_duplicated) != 0:
            self.notification_services.show_warnning(f"Hay persona duplicadas: {str(persons_duplicated)}")

        if len(persons_name_not_found_in_db) != 0:
            self.notification_services.show_warnning(f"Hay persona que no estan en la base de datos: {str(persons_name_not_found_in_db)}")
