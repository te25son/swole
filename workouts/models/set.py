from dataclasses import dataclass

from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.fields import Field

from workouts.models.generic.entity import Entity

from .exercise import Exercise
from .measurementUnits import MeasurementUnits
from .workout import Workout


@dataclass
class SetCreate:
    workout: Workout
    exercise: Exercise
    weight: int | None = None
    rep_count: int | None = None


class Set(Entity):
    exercise: Field = models.ForeignKey(to=Exercise, on_delete=models.CASCADE)
    workout: Field = models.ForeignKey(to=Workout, on_delete=models.CASCADE)
    weight: Field = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(2000, message="Weight cannot be greater than 2000.")
        ],
    )
    unit: Field = models.CharField(
        max_length=3,
        choices=MeasurementUnits.choices,
        default=MeasurementUnits.KILOGRAMS,
        blank=True,
    )
    rep_count: Field = models.PositiveSmallIntegerField(default=0)
    created_datetime: Field = models.DateTimeField(
        auto_now_add=True
    )  # This is not UTC. Timezone is defined by the TIME_ZONE setting.
    name: Field = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "workouts"
