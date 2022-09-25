import calendar
import datetime
import jwt
from flask import request, abort

from implemented import user_service
from constants import JWT_SECRET, JWT_ALGO


def generate_token(data: dict, refresh=False) -> str:
    """
    Generate token using JWT

    :param data: Payload for the token
    :param refresh: False: use default expiration time of 30 minutes;
                    True: set expiration time to 130 days
    """
    if refresh:
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    else:
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    data['exp'] = calendar.timegm(exp_time.timetuple())
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)


def decode_token(token: str) -> dict | None:
    """
    Decode a JWT token
    """
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.exceptions.InvalidTokenError:
        return None
    return data


def auth_required(func):
    """
    Decorator for Flask views that checks for a valid auth token
    """
    def wrapper(*args, **kwargs):
        auth_data = request.headers.get('Authorization')
        if not auth_data:
            abort(401)

        token = auth_data.split('Bearer ')[-1]

        if not decode_token(token):
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    Decorator for Flask views that checks if the user has the 'admin' role

    Also checks validity of the auth token
    """
    def wrapper(*args, **kwargs):
        auth_data = request.headers.get('Authorization')
        if not auth_data:
            abort(401)

        token = auth_data.split('Bearer ')[-1]
        user_data = decode_token(token)

        if user_data is None:
            abort(401)

        user = user_service.get_by_username(user_data.get('username'))

        if user.role != 'admin':
            abort(401)
        return func(*args, **kwargs)

    return wrapper
