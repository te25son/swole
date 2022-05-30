from typing import List
from uuid import UUID

from users.models import User
from workouts.logic.base_repository import Repository
from workouts.models import Exercise
from workouts.models.exercise import ExerciseCreate, ExerciseUpdate


def get_all() -> List[Exercise]:
    return list(Exercise.objects.all())


def user_has_existing_exercises(user: User) -> bool:
    return any(Exercise.objects.filter(workouts__user=user))


def get_user_exercises(user: User) -> List[Exercise]:
    return list(Exercise.objects.filter(workouts__user=user).distinct())


class ExerciseRepository(Repository[Exercise]):
    @staticmethod
    def get_by_id(id: UUID) -> Exercise:
        return Exercise.objects.get(id=id)

    @staticmethod
    def get_all_by_user(user: User) -> List[Exercise]:
        return list(Exercise.objects.filter(workouts__user=user).order_by("name").distinct())

    @staticmethod
    def get_all_by_workout(workout_id: UUID) -> List[Exercise]:
        return list(Exercise.objects.filter(workouts__id=workout_id))

    @staticmethod
    def create(exercise: ExerciseCreate) -> Exercise:
        new_exercsise = Exercise(name=exercise.name)
        new_exercsise.save()
        new_exercsise.workouts.add(*exercise.workouts)
        return new_exercsise

    @staticmethod
    def delete(exercise: Exercise) -> None:
        pass

    @staticmethod
    def update(exercise: ExerciseUpdate) -> Exercise:
        pass
