from flask_restx import Resource, Namespace
from implemented import genre_service, genre_schema

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresViews(Resource):
    def get(self):
        all_genres = genre_service.get_all()
        return genre_schema.dump(all_genres, many=True), 200


@genre_ns.route('/<int:gid>')
class GenreViews(Resource):
    def get(self, gid):
        genre = genre_service.get_by_id(gid)
        return genre_schema.dump(genre), 200
