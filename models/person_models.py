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
