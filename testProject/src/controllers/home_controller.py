# from flask import Blueprint, render_template
#
# home_controller = Blueprint('home_controller', __name__)
#
#
# @home_controller.route('/')
# def home():
#     return render_template('home/home.html', title='Home Page')
#

from flask import Blueprint, render_template, g

home_controller = Blueprint('home_controller', __name__)


@home_controller.route('/')
def home():
    return render_template('home/home.html', title='Home Page', is_authenticated=bool(g.user))

