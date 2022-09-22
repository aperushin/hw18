from .model.models import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> list[Director]:
        query = self.session.query(Director)
        return query.all()

    def get_by_id(self, did: int) -> Director:
        query = self.session.query(Director)
        return query.get(did)
