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
