from dao.movie import MovieDAO
from dao.model.models import Movie, MovieSchema


class MovieService:

    SUPPORTED_FILTERS = ('genre_id', 'director_id', 'year')

    def __init__(self, movies_dao: MovieDAO):
        self.movies_dao: MovieDAO = movies_dao

    @staticmethod
    def _validate(movie_data) -> dict:
        validated_data = MovieSchema().load(movie_data)
        return validated_data

    def get_all(self) -> list[Movie]:
        return self.movies_dao.get_all()

    def get_by_id(self, mid):
        return self.movies_dao.get_by_id(mid)

    def get_by_filters(self, filters: dict) -> list[Movie]:
        filters = filter_dict(filters, allowed_keys=self.SUPPORTED_FILTERS)
        return self.movies_dao.get_by_filters(filters)

    def create(self, movie_data: dict) -> Movie:
        movie_data = self._validate(movie_data)
        new_movie = Movie(**movie_data)
        movie_added = self.movies_dao.add(new_movie)
        return movie_added

    def update(self, mid: int, movie_data: dict) -> bool:
        movie: Movie = self.movies_dao.get_by_id(mid)
        if not movie:
            return False

        new_movie_data = self._validate(movie_data)

        self.movies_dao.update(mid, new_movie_data)
        return True

    def delete(self, mid: int) -> bool:
        movie = self.movies_dao.get_by_id(mid)
        if not movie:
            return False

        self.movies_dao.delete(movie)
        return True


def filter_dict(dictionary: dict, allowed_keys: list | tuple) -> dict:
    """
    Remove key from a dictionary if it is not in the list of allowed keys.
    """
    return {k: v for k, v in dictionary.items() if k in allowed_keys}
