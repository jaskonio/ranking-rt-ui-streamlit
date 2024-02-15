from services.notification_service import NotificationServices
from services.request_services import RequestServices
from services.config_services import ConfigServices

class RacesServices():
    hostname = ConfigServices.getBackendConfig('url')

    def __init__(self, requestServices:RequestServices, notificationServices:NotificationServices) -> None:
        self.notification_services = notificationServices
        self.request_services = requestServices

    def get_all(self):
        url = self.hostname + "/races"
        response = self.request_services.get(url)
        return response.json()

    def get_by_id(self, race_id):
        url = self.hostname + "/races/" + race_id
        response = self.request_services.get(url)

        if response.status_code != 200:
            self.notification_services.show_warnning("Hubo un error al actualizar")
            return []

        return response.json()

    def update(self, race):
        url = self.hostname + "/races/" + race["id"]
        response = self.request_services.put(url, json=race)

        if response.status_code == 200:
            self.notification_services.show_info("Se ha actualizado correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al actualizar")
        return False, response.json()

    def add(self, race):
        url = self.hostname + "/races"
        response = self.request_services.post(url, json=race)
        if response.status_code == 200:
            self.notification_services.show_info("Se ha añadido correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al añadir")
        return False, response.json()

    def delete(self, race_id):
        url = self.hostname + "/races/" + race_id
        response = self.request_services.delete(url)
        if response.status_code == 200:
            self.notification_services.show_info("Se ha eliminado correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al eliminar")
        return False, response.json()

    def process(self, race_id):
        url = self.hostname + "/races/run/" + race_id
        response = self.request_services.get(url)
        if response.status_code == 200:
            self.notification_services.show_info("Se ha processado correctamente")
            return True, []

        self.notification_services.show_warnning("Hubo un error al processar")
        return False, response.json()
