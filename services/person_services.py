from services.notification_service import NotificationServices
from services.request_services import RequestServices

class PersonServices():
    hostname = "http://localhost:8000"

    def __init__(self, requestServices:RequestServices, notificationServices:NotificationServices) -> None:
        self.notification_services = notificationServices
        self.request_services = requestServices

    def get_all(self):
        url = self.hostname + "/persons"
        response = self.request_services.get(url)
        person_json = response.json()
        for person in person_json:
            person["photo_url"] = self.hostname + person["photo_url"]
        return person_json

    def update_person(self, person):
        url = self.hostname + "/persons/" + person["id"]
        response = self.request_services.put(url, json=person)

        if response.status_code == 200:
            self.notification_services.show_info("Se ha actualizado correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al actualizar")
        return False, response.json()

    def add_person(self, person):
        url = self.hostname + "/persons"
        response = self.request_services.post(url, json=person)
        if response.status_code == 200:
            self.notification_services.show_info("Se ha añadido correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al añadir")
        return False, response.json()
