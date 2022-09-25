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
    
    def add(self, genre: Genre) -> Genre:
        self.session.add(genre)
        self.session.commit()
        return genre

    def update(self, gid: int, genre_data: dict):
        self.session.query(Genre).filter_by(id=gid).update(genre_data)
        self.session.commit()

    def delete(self, genre: Genre) -> None:
        self.session.delete(genre)
        self.session.commit()
