from flask import g, request
from .decorators import use_db
from .models import User


def get_ip():
    # Since using ProxyFix, Deosn't need to parse X-Forwarded-For
    return request.remote_addr


@use_db
def get_user():
    ip = get_ip()
    user = g.db.query(User).get(ip)
    if user:
        return user

    user = User(ip=ip)
    g.db.add(user)
    g.db.commit()

    return user
