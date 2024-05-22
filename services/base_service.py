from services.config_services import ConfigServices
from services.notification_service import NotificationServices
from services.request_services import RequestServices

class BaseServices():
    hostname = ConfigServices.getBackendConfig('url')

    def __init__(self, request_services:RequestServices, notification_services:NotificationServices, endpoint:str) -> None:
        self.request_services = request_services
        self.notification_services = notification_services
        self.endpoint = endpoint
        self.base_url = self.hostname + "/" + self.endpoint

    def add(self, json_data):
        print(json_data)
        url = self.base_url
        response = self.request_services.post(url, json=json_data)

        if response.status_code != 200:
            self.notification_services.show_warnning("Hubo un error al añadir")
            return None

        self.notification_services.show_info("Se ha añadido correctamente")
        return response.json()['data']

    def get_by_id(self, id=str):
        url = self.base_url + "/" + id
        response = self.request_services.get(url)

        if response.status_code != 200:
            self.notification_services.show_warnning("Hubo un error al recuperar los datos")
            return None

        self.notification_services.show_info("Se ha actualizado correctamente")
        return response.json()['data']

    def update(self, json_data):
        url = self.base_url + "/" + json_data["id"]
        response = self.request_services.put(url, json=json_data)

        if response.status_code != 201:
            self.notification_services.show_warnning("Hubo un error al actualizar")
            return None

        self.notification_services.show_info("Se ha actualizado correctamente")
        return response.json()['data']

    def get_all(self):
        url = self.base_url
        response = self.request_services.get(url)

        if response.status_code != 200:
            self.notification_services.show_warnning("Hubo un error al recuperar los datos")
            return None

        return response.json()['data']

    def delete(self, id):
        url = self.base_url + "/" + id
        response = self.request_services.delete(url)

        if response.status_code != 200:
            self.notification_services.show_warnning("Hubo un error al eliminar")
            return None

        self.notification_services.show_info("Se ha eliminado correctamente")
        return True
