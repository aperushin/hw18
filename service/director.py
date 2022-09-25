from dao.director import DirectorDAO
from dao.model.models import Director, DirectorSchema


class DirectorService:

    def __init__(self, directors_dao: DirectorDAO):
        self.directors_dao: DirectorDAO = directors_dao

    @staticmethod
    def _validate(director_data) -> dict:
        validated_data = DirectorSchema().load(director_data)
        return validated_data

    def get_all(self) -> list[Director]:
        return self.directors_dao.get_all()

    def get_by_id(self, did):
        return self.directors_dao.get_by_id(did)
    
    def create(self, director_data: dict) -> Director:
        director_data = self._validate(director_data)
        new_director = Director(**director_data)
        director_added = self.directors_dao.add(new_director)
        return director_added

    def update(self, did: int, director_data: dict) -> bool:
        director: Director = self.directors_dao.get_by_id(did)
        if not director:
            return False

        new_director_data = self._validate(director_data)

        self.directors_dao.update(did, new_director_data)
        return True

    def delete(self, did: int) -> bool:
        director = self.directors_dao.get_by_id(did)
        if not director:
            return False

        self.directors_dao.delete(director)
        return True
