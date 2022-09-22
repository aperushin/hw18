from flask import request
from flask_restx import Resource, Namespace
from implemented import movie_service, movie_schema
from marshmallow.exceptions import ValidationError

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesViews(Resource):
    def get(self):
        filters = request.args.to_dict()

        if filters:
            all_movies = movie_service.get_by_filters(filters)
        else:
            all_movies = movie_service.get_all()

        return movie_schema.dump(all_movies, many=True), 200

    def post(self):
        movie_data = request.json

        try:
            movie_added = movie_service.create(movie_data)
        except ValidationError:
            return '', 400

        return '', 201, {'location': f'/movies/{movie_added.id}'}


@movie_ns.route('/<int:mid>')
class MovieViews(Resource):
    def get(self, mid):
        movie = movie_service.get_by_id(mid)
        if not movie:
            return '', 404
        return movie_schema.dump(movie), 200

    def put(self, mid):
        movie_data = request.json

        try:
            result = movie_service.update(mid, movie_data)
        except ValidationError:
            return '', 400

        if not result:
            return '', 404

        return '', 204

    def delete(self, mid):
        result = movie_service.delete(mid)
        if not result:
            return '', 404
        return '', 204
