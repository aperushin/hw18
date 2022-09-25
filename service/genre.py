from dao.genre import GenreDAO
from dao.model.models import Genre, GenreSchema


class GenreService:

    def __init__(self, genres_dao: GenreDAO):
        self.genres_dao: GenreDAO = genres_dao

    @staticmethod
    def _validate(genre_data) -> dict:
        validated_data = GenreSchema().load(genre_data)
        return validated_data

    def get_all(self) -> list[Genre]:
        return self.genres_dao.get_all()

    def get_by_id(self, did):
        return self.genres_dao.get_by_id(did)
    
    def create(self, genre_data: dict) -> Genre:
        genre_data = self._validate(genre_data)
        new_genre = Genre(**genre_data)
        genre_added = self.genres_dao.add(new_genre)
        return genre_added

    def update(self, gid: int, genre_data: dict) -> bool:
        genre: Genre = self.genres_dao.get_by_id(gid)
        if not genre:
            return False

        new_genre_data = self._validate(genre_data)

        self.genres_dao.update(gid, new_genre_data)
        return True

    def delete(self, gid: int) -> bool:
        genre = self.genres_dao.get_by_id(gid)
        if not genre:
            return False

        self.genres_dao.delete(genre)
        return True
