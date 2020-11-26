from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .exercisemanager.exercisemanager import ExerciseManager
from . import cache

exercise_manager = ExerciseManager()

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
@cache.cached(timeout=10)
def profile():
    exercise = exercise_manager.get_exer_for_user(current_user.id)

    return render_template('profile.html',
                           name=current_user.name,
                           exercise=exercise)
