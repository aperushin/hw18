from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from implemented import director_service, director_schema
from auth.auth import admin_required, auth_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsViews(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all()
        return director_schema.dump(all_directors, many=True), 200

    @admin_required
    def post(self):
        director_data = request.json

        try:
            director_added = director_service.create(director_data)
        except ValidationError:
            return '', 400

        return '', 201, {'location': f'/directors/{director_added.id}'}


@director_ns.route('/<int:did>')
class DirectorViews(Resource):
    @auth_required
    def get(self, did):
        director = director_service.get_by_id(did)
        if not director:
            return '', 404
        return director_schema.dump(director), 200

    @admin_required
    def put(self, did):
        director_data = request.json

        try:
            result = director_service.update(did, director_data)
        except ValidationError:
            return '', 400

        if not result:
            return '', 404

        return '', 204

    @admin_required
    def delete(self, did):
        result = director_service.delete(did)
        if not result:
            return '', 404
        return '', 204
