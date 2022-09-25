from flask import request, abort
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from implemented import user_service, user_schema
from auth.auth import admin_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersViews(Resource):
    @admin_required
    def get(self):
        all_users = user_service.get_all()
        return user_schema.dump(all_users, many=True), 200

    @admin_required
    def post(self):
        user_data = request.json

        try:
            user_added = user_service.create(user_data)
        except ValidationError:
            abort(400)
        except IntegrityError:
            return {'message': 'user already exists'}, 400

        return '', 201, {'location': f'/users/{user_added.id}'}


@user_ns.route('/<int:uid>')
class UserViews(Resource):
    @admin_required
    def get(self, uid):
        user = user_service.get_by_id(uid)
        if not user:
            return '', 404
        return user_schema.dump(user), 200

    @admin_required
    def put(self, uid):
        user_data = request.json

        try:
            result = user_service.update(uid, user_data)
        except ValidationError:
            return '', 400

        if not result:
            return '', 404

        return '', 204

    @admin_required
    def delete(self, uid):
        result = user_service.delete(uid)
        if not result:
            return '', 404
        return '', 204
