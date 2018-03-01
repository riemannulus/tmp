from flask import g, request
from .decorators import use_db
from .models import User


def get_ip():
    forwarded = request.headers.getlist('X-Forwarded-For')
    if forwarded:
        return forwarded[0]

    return request.remote_addr


@use_db
def get_user():
    ip = get_ip()
    user = g.db.query(User).get(ip)
    if user:
        return user

    user = User(ip=ip)
    g.db.add(user)

    return user
