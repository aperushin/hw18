from .model.models import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> list[Movie]:
        query = self.session.query(Movie)
        return query.all()

    def get_by_id(self, mid: int) -> Movie:
        query = self.session.query(Movie)
        return query.get(mid)

    def get_by_filters(self, filters: dict) -> list[Movie]:
        query = self.session.query(Movie)
        return query.filter_by(**filters).all()

    def add(self, movie: Movie) -> Movie:
        self.session.add(movie)
        self.session.commit()
        return movie

    def update(self, mid: int, movie_data: dict):
        self.session.query(Movie).filter_by(id=mid).update(movie_data)
        self.session.commit()

    def delete(self, movie: Movie) -> None:
        self.session.delete(movie)
        self.session.commit()
