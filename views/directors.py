from flask_restx import Resource, Namespace
from implemented import director_service, director_schema

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsViews(Resource):
    def get(self):
        all_directors = director_service.get_all()
        return director_schema.dump(all_directors, many=True), 200


@director_ns.route('/<int:did>')
class DirectorViews(Resource):
    def get(self, did):
        director = director_service.get_by_id(did)
        return director_schema.dump(director), 200
