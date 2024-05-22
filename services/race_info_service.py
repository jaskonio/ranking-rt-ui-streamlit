from services.base_service import BaseServices
from services.notification_service import NotificationServices
from services.request_services import RequestServices


class RaceInfoService(BaseServices):
    def __init__(self, request_services:RequestServices, notification_services:NotificationServices) ->None:
        super().__init__(request_services, notification_services, 'raceinfo')
    
    def process_by_id(self, race_id):
        url = self.base_url + "/run_process/" + str(race_id)
        response = self.request_services.get(url)

        if response.status_code != 200:
            self.notification_services.show_warnning("Hubo un error al recuperar los datos")
            return None

        self.notification_services.show_info("Se ha actualizado correctamente")
        return response.json()['data']
