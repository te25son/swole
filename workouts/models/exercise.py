from dataclasses import dataclass
from typing import List

from django.contrib.postgres.fields import CICharField
from django.db import models
from django.db.models.fields import Field

from workouts.models.generic.entity import Entity, EntityCreate, EntityUpdate

from .workout import Workout


@dataclass
class ExerciseCreate(EntityCreate):
    name: str
    workouts: List[Workout]


class ExerciseUpdate(EntityUpdate):
    pass


class Exercise(Entity):
    name: Field = CICharField(max_length=150, unique=True)
    workouts: Field = models.ManyToManyField(to=Workout)

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "workouts"
