from dao.director import DirectorDAO
from dao.model.models import Director


class DirectorService:

    def __init__(self, directors_dao: DirectorDAO):
        self.directors_dao: DirectorDAO = directors_dao

    def get_all(self) -> list[Director]:
        return self.directors_dao.get_all()

    def get_by_id(self, did):
        return self.directors_dao.get_by_id(did)
