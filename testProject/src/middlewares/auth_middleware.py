from flask import request, redirect, g, make_response
from src.lib.jwt import JWT
import os
from functools import wraps
from flask import session, redirect, url_for

JWT_SECRET = os.getenv('JWT_SECRET', 'your_jwt_secret_here')
AUTH_COOKIE_NAME = 'auth'


def auth_middleware():
    """
    Middleware logic to check JWT token in cookies.
    - If token exists and is valid, store user info in `g.user`.
    - If no token or invalid, redirect to login.
    """
    token = request.cookies.get(AUTH_COOKIE_NAME)

    if token:
        try:
            decoded_token = JWT.verify(token, JWT_SECRET)
            g.user = decoded_token
            g.is_authenticated = True
        except Exception:
            response = make_response(redirect('/auth/login'))
            response.set_cookie(AUTH_COOKIE_NAME, '', expires=0)
            return response
    else:
        g.user = None
        g.is_authenticated = False


def login_required(f):
    """
    Decorator to protect routes that require authentication.
    Redirects to login page if user is not authenticated.
    """
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not getattr(g, 'user', None):
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function

