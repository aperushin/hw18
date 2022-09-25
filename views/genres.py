from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from implemented import genre_service, genre_schema
from auth.auth import admin_required, auth_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresViews(Resource):
    @auth_required
    def get(self):
        all_genres = genre_service.get_all()
        return genre_schema.dump(all_genres, many=True), 200

    @admin_required
    def post(self):
        genre_data = request.json

        try:
            genre_added = genre_service.create(genre_data)
        except ValidationError:
            return '', 400

        return '', 201, {'location': f'/genres/{genre_added.id}'}


@genre_ns.route('/<int:gid>')
class GenreViews(Resource):
    @auth_required
    def get(self, gid):
        genre = genre_service.get_by_id(gid)
        if not genre:
            return '', 404
        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, gid):
        genre_data = request.json

        try:
            result = genre_service.update(gid, genre_data)
        except ValidationError:
            return '', 400

        if not result:
            return '', 404

        return '', 204

    @admin_required
    def delete(self, gid):
        result = genre_service.delete(gid)
        if not result:
            return '', 404
        return '', 204
