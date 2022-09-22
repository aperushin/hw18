from dao.genre import GenreDAO
from dao.model.models import Genre


class GenreService:

    def __init__(self, genres_dao: GenreDAO):
        self.genres_dao: GenreDAO = genres_dao

    def get_all(self) -> list[Genre]:
        return self.genres_dao.get_all()

    def get_by_id(self, did):
        return self.genres_dao.get_by_id(did)
