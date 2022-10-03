from unittest.mock import MagicMock

import pytest
from dao.director import DirectorDAO
from dao.model.models import Director
from service.director import DirectorService


@pytest.fixture
def director_dao_mock():
    directors = [
        Director(id=1, name='test'),
        Director(id=2, name='test2'),
        Director(id=3, name='test3')
    ]
    dao = DirectorDAO(None)
    dao.get_by_id = MagicMock(return_value=directors[0])
    dao.get_all = MagicMock(return_value=directors)
    dao.add = MagicMock(return_value=directors[2])
    dao.update = MagicMock(return_value=True)
    dao.delete = MagicMock(return_value=True)
    return dao


class TestDirectorService:

    @pytest.fixture
    def director_service(self, director_dao_mock) -> DirectorService:
        return DirectorService(director_dao_mock)

    def test_get_all(self, director_service):
        all_directors = director_service.get_all()
        assert all_directors
        assert isinstance(all_directors, list)

    def get_by_id(self, director_service):
        director = director_service.get_by_id(1)
        assert isinstance(director, Director)

    def test_create(self, director_service):
        result = director_service.create({'name': 'test'})
        assert isinstance(result, Director)

    def test_update(self, director_service):
        result = director_service.update(1, {'name': 'test'})
        assert result

    def test_update_not_found(self, director_service, director_dao_mock):
        director_dao_mock.get_by_id.return_value = None
        assert not director_service.update(-1, {'name': 'test'})

    def test_delete(self, director_service):
        assert director_service.delete(1)

    def test_delete_not_found(self, director_service, director_dao_mock):
        director_dao_mock.get_by_id.return_value = None
        assert not director_service.delete(1)
