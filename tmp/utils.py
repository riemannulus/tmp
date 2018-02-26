from flask import request


def get_ip():
    forwarded = request.headers.getlist('X-Forwarded-For')
    if forwarded:
        return forwarded[0]

    return request.remote_addr
