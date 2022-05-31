from typing import List
from uuid import UUID

from users.models import User
from workouts.logic.base_repository import Repository
from workouts.models import Workout
from workouts.models.workout import WorkoutCreate, WorkoutUpdate


def copy_workout(id: UUID) -> Workout:
    original: Workout = Workout.objects.get(pk=id)
    original.pk = None
    original.id = None
    original._state.adding = True
    original.save()

    return original


class WorkoutRepository(Repository[Workout]):
    @staticmethod
    def get_by_id(id: UUID) -> Workout:
        return Workout.objects.get(id=id)

    @staticmethod
    def get_all_by_user(user: User, deleted: bool = False) -> List[Workout]:
        queryset = Workout.all_objects if deleted else Workout.objects
        return list(queryset.filter(user=user).order_by("-date"))

    @staticmethod
    def create(workout: WorkoutCreate) -> Workout:
        new_workout = Workout(name=workout.name, date=workout.date, user=workout.user)
        new_workout.save()
        return new_workout

    @staticmethod
    def update(workout: WorkoutUpdate) -> Workout:
        pass

    @staticmethod
    def delete(workout: Workout) -> None:
        pass
