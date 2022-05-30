from typing import List
from uuid import UUID

from workouts.models import Set, SetCreate

from .base_repository import Repository


class SetRepository(Repository[Set]):
    @staticmethod
    def get_by_id(id: UUID) -> Set:
        return Set.objects.get(id=id)

    @staticmethod
    def get_all_by_workout_and_exercise(
        workout_id: UUID, exercise_id: UUID
    ) -> List[Set]:
        return list(
            Set.objects.filter(
                workout__id=workout_id, exercise__id=exercise_id
            ).order_by("name")
        )

    @classmethod
    def create(cls, set: SetCreate) -> Set:
        workout = set.workout
        exercise = set.exercise
        related_sets = cls.get_all_by_workout_and_exercise(workout.id, exercise.id)
        new_set = Set(
            workout=workout,
            exercise=exercise,
            weight=set.weight,
            rep_count=set.rep_count,
            name=f"Set {len(related_sets) + 1}",
        )
        new_set.save()
        return new_set

    @classmethod
    def delete(cls, set: Set) -> None:
        workout_id = set.workout.id
        exercise_id = set.exercise.id
        set.delete()
        cls._rename_sets(workout_id, exercise_id)

    @classmethod
    def update(cls, set: Set) -> None:
        pass

    @classmethod
    def _rename_sets(cls, workout_id: UUID, exercise_id: UUID) -> None:
        sets = cls.get_all_by_workout_and_exercise(workout_id, exercise_id)

        for count, set in enumerate(sets):
            set.name = f"Set {count + 1}"
            set.save()
