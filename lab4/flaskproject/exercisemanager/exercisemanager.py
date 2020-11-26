from random import choice
from ..dataaccesslayer.CRUD import get_all_user_exercises


class ExerciseManager():
    def get_exer_for_user(self, user_id):
        all_user_exercises = [exer.name for exer
                              in get_all_user_exercises(user_id)]

        if all_user_exercises:
            return choice(all_user_exercises)
        return "Choose your exersices first \u2B07"
