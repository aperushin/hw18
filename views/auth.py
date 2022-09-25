from flask import request, abort
from flask_restx import Resource, Namespace
from implemented import user_service
from auth.auth import generate_token, decode_token

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthViews(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if not all([username, password]):
            abort(400)

        user = user_service.get_by_username(username)
        if user is None:
            return {'message': 'user not found'}, 401

        is_correct_password = user_service.compare_passwords(
            password,
            user.password
        )

        if not is_correct_password:
            return {'message': 'incorrect password'}, 401

        user_data = {'username': user.username, 'role': user.role}

        access_token = generate_token(user_data)
        refresh_token = generate_token(user_data, refresh=True)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201

    def put(self):
        refresh_token = request.json.get('refresh_token')
        if not refresh_token:
            abort(400)

        user_data = decode_token(refresh_token)
        if user_data is None:
            return {'message': 'invalid token'}, 401

        access_token = generate_token(user_data)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
