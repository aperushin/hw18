from unittest.mock import MagicMock

import pytest
from dao.genre import GenreDAO
from dao.model.models import Genre
from service.genre import GenreService


@pytest.fixture
def genre_dao_mock():
    genres = [
        Genre(id=1, name='test'),
        Genre(id=2, name='test2'),
        Genre(id=3, name='test3')
    ]
    dao = GenreDAO(None)
    dao.get_by_id = MagicMock(return_value=genres[0])
    dao.get_all = MagicMock(return_value=genres)
    dao.add = MagicMock(return_value=genres[2])
    dao.update = MagicMock(return_value=True)
    dao.delete = MagicMock(return_value=True)
    return dao


class TestGenreService:

    @pytest.fixture
    def genre_service(self, genre_dao_mock) -> GenreService:
        return GenreService(genre_dao_mock)

    def test_get_all(self, genre_service):
        all_genres = genre_service.get_all()
        assert all_genres
        assert isinstance(all_genres, list)

    def get_by_id(self, genre_service):
        genre = genre_service.get_by_id(1)
        assert isinstance(genre, Genre)

    def test_create(self, genre_service):
        result = genre_service.create({'name': 'test'})
        assert isinstance(result, Genre)

    def test_update(self, genre_service):
        result = genre_service.update(1, {'name': 'test'})
        assert result

    def test_update_not_found(self, genre_service, genre_dao_mock):
        genre_dao_mock.get_by_id.return_value = None
        assert not genre_service.update(-1, {'name': 'test'})

    def test_delete(self, genre_service):
        assert genre_service.delete(1)

    def test_delete_not_found(self, genre_service, genre_dao_mock):
        genre_dao_mock.get_by_id.return_value = None
        assert not genre_service.delete(1)
