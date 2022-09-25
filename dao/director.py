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

    def add(self, director: Director) -> Director:
        self.session.add(director)
        self.session.commit()
        return director

    def update(self, did: int, director_data: dict):
        self.session.query(Director).filter_by(id=did).update(director_data)
        self.session.commit()

    def delete(self, director: Director) -> None:
        self.session.delete(director)
        self.session.commit()
