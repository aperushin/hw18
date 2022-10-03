from unittest.mock import MagicMock

import pytest
from dao.movie import MovieDAO
from dao.model.models import Movie
from service.movie import MovieService


@pytest.fixture
def movie_dao_mock():
    movies = [
        Movie(id=1,
              title='test',
              description='test',
              trailer='test',
              year=1970,
              rating=8.6,
              genre_id=1,
              director_id=1
              ),
        Movie(id=2,
              title='test2',
              description='test2',
              trailer='test2',
              year=1971,
              rating=8.8,
              genre_id=2,
              director_id=2
              ),
    ]
    dao = MovieDAO(None)
    dao.get_by_id = MagicMock(return_value=movies[0])
    dao.get_all = MagicMock(return_value=movies)
    dao.add = MagicMock(return_value=movies[1])
    dao.update = MagicMock(return_value=True)
    dao.delete = MagicMock(return_value=True)
    return dao


class TestMovieService:

    @pytest.fixture
    def movie_service(self, movie_dao_mock) -> MovieService:
        return MovieService(movie_dao_mock)

    def test_get_all(self, movie_service):
        all_movies = movie_service.get_all()
        assert all_movies
        assert isinstance(all_movies, list)

    def get_by_id(self, movie_service):
        movie = movie_service.get_by_id(1)
        assert isinstance(movie, Movie)

    def test_create(self, movie_service):
        result = movie_service.create({
            "title": "test",
            "description": "test",
            "trailer": "test",
            "year": 2018,
            "rating": 8.6,
            "genre_id": 17,
            "director_id": 1
        })
        assert isinstance(result, Movie)

    def test_update(self, movie_service):
        result = movie_service.update(1, {
            "title": "test",
            "description": "test",
            "trailer": "test",
            "year": 2018,
            "rating": 8.6,
            "genre_id": 17,
            "director_id": 1
        })
        assert result

    def test_update_not_found(self, movie_service, movie_dao_mock):
        movie_dao_mock.get_by_id.return_value = None
        assert not movie_service.update(-1, {})

    def test_delete(self, movie_service):
        assert movie_service.delete(1)

    def test_delete_not_found(self, movie_service, movie_dao_mock):
        movie_dao_mock.get_by_id.return_value = None
        assert not movie_service.delete(1)
