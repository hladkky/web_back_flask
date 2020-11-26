from .. import db
from ..models import User, Exercise, UsersExercises
from .. import cache


@cache.cached(key_prefix='get_all_exercises')
def get_all_exercises():
    return Exercise.query.all()


def get_all_user_exercises(user_id):
    "Return list of Exercise's objects"
    return db.session.query(
        Exercise
    ).join(UsersExercises).filter(UsersExercises.idU == user_id).all()


def update_user_exercises(user_id, choosen_exercises_names):
    choosen_exercises = [exer.id for exer in Exercise.query.filter(
        Exercise.name.in_(choosen_exercises_names)
    ).all()]
    current_exercises = [exer.id for exer in get_all_user_exercises(user_id)]

    for exer in get_all_exercises():
        if exer.id in current_exercises and exer.id not in choosen_exercises:
            UsersExercises.query.filter(
                UsersExercises.idU == user_id and UsersExercises.idE == exer.id
            ).delete()
            print('delete')
        elif exer.id not in current_exercises and exer.id in choosen_exercises:
            newUE = UsersExercises(idU=user_id, idE=exer.id)
            db.session.add(newUE)

    db.session.commit()
