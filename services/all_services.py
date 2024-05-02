from services.base_service import BaseServices
from services.notification_service import NotificationServices
from services.race_info_service import RaceInfoService
from services.request_services import RequestServices

request_service = RequestServices()
notification_service = NotificationServices()

race_info_service = RaceInfoService(request_service, notification_service)
person_service = BaseServices(request_service, notification_service, 'persons')
image_service = BaseServices(request_service, notification_service, 'image')

season_service = BaseServices(request_service, notification_service, 'season')
leagues_service = BaseServices(request_service, notification_service, 'leagues')
race_league_service = BaseServices(request_service, notification_service, 'race_league')
participant_league_service = BaseServices(request_service, notification_service, 'participant_league')
ranking_league_service = BaseServices(request_service, notification_service, 'ranking_league')
