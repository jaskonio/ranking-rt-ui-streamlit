from services.notification_service import NotificationServices
from services.request_services import RequestServices

class LeagueServices():
    hostname = "http://localhost:8000"

    def __init__(self, requestServices:RequestServices, notificationServices:NotificationServices) -> None:
        self.notification_services = notificationServices
        self.request_services = requestServices

    def get_all(self):
        url = self.hostname + "/leagues"
        response = self.request_services.get(url)
        return response.json()

    def update(self, league):
        url = self.hostname + "/leagues/" + league["id"]
        response = self.request_services.put(url, json=league)

        if response.status_code == 200:
            self.notification_services.show_info("Se ha actualizado correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al actualizar")
        return False, response.json()

    def add(self, league):
        url = self.hostname + "/leagues"
        response = self.request_services.post(url, json=league)
        if response.status_code == 200:
            self.notification_services.show_info("Se ha añadido correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al añadir")
        return False, response.json()

    def get_all_filter_by_property(self, property_name):
        all_league = self.get_all()
        if all_league is None or len(all_league) == 0:
            return None

        league_filtered = []
        if property_name in all_league[0]:
            league_filtered = [league[property_name] for league in all_league]

        return league_filtered

    def get_all_names(self):
        return self.get_all_filter_by_property('name')

    def add_runners_by_league_id(self, league_id, runners):
        url = self.hostname + "/leagues/"+ str(league_id) + "/add_runners"
        response = self.request_services.post(url, json=runners)

        if response.status_code == 200:
            self.notification_services.show_info("Se han añadido correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al añadir los runners")
        return False, response.json()
