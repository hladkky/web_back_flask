from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user
from .CRUD import get_all_exercises, get_all_user_exercises,\
                 update_user_exercises

DAL = Blueprint('DAL', __name__)


@DAL.route('/choose_exercises')
@login_required
def choose_exercises():
    exers = get_all_exercises()
    user_exers = [exer.name
                  for exer in get_all_user_exercises(current_user.id)]

    return render_template("choose_exercises.html",
                           exercises=[exer.name for exer in exers],
                           current=user_exers)


@DAL.route('/choose_exercises', methods=['POST'])
def choose_exercises_post():
    choosen_exercises_names = list(request.form.keys())
    update_user_exercises(current_user.id, choosen_exercises_names)
    return redirect(url_for("main.profile"))
