from .model.models import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> list[Genre]:
        query = self.session.query(Genre)
        return query.all()

    def get_by_id(self, gid: int) -> Genre:
        query = self.session.query(Genre)
        return query.get(gid)
