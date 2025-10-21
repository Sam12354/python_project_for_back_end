# src/controllers/auth_controller.py
#convert your Express.js authController into a Flask

from flask import Blueprint, render_template, make_response
from src.services.auth_service import AuthService
from src.utils.error_utils import get_error_message

import os
from flask import session, request, redirect, make_response, render_template, url_for

auth_controller = Blueprint('auth_controller', __name__)
AUTH_COOKIE_NAME = os.getenv('AUTH_COOKIE_NAME', 'auth')


@auth_controller.route('/register', methods=['GET'])
def register_get():
    return render_template('auth/register.html', title='Register Page')


@auth_controller.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    re_pass = request.form.get('rePass')

    try:
        from src.config.db_config import SessionLocal  # lazy import to avoid circular issue
        db = SessionLocal()
        token = AuthService.register(db, username, email, password, re_pass)
        response = make_response(redirect('/'))
        response.set_cookie(AUTH_COOKIE_NAME, token, httponly=True)
        return response
    except Exception as err:
        error = get_error_message(err)
        return render_template('auth/register.html', title='Register Page', username=username, email=email, error=error)


@auth_controller.route('/login', methods=['GET'])
def login_get():
    return render_template('auth/login.html', title='Login Page')


import logging


@auth_controller.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    logging.info(f"Login attempt for email: {email}")

    try:
        from src.config.db_config import SessionLocal
        db = SessionLocal()

        user, token = AuthService.login(db, email, password)
        logging.info(f"User found: {user.id}, Token generated")

        session['user_id'] = user.id

        response = make_response(redirect(url_for('home_controller.home')))
        response.set_cookie(AUTH_COOKIE_NAME, token, httponly=True)
        logging.info("Redirecting to home and setting cookie")
        return response
    except Exception as err:
        logging.error(f"Login error: {err}")
        error = get_error_message(err)
        return render_template('auth/login.html', title='Login Page', email=email, error=error)


@auth_controller.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie(AUTH_COOKIE_NAME, '', expires=0)
    return response
