from dataclasses import dataclass
from datetime import datetime

from django.conf import settings
from django.contrib.postgres.fields import CICharField
from django.db import models
from django.db.models.fields import Field

from users.models import User
from workouts.models.generic.entity import EntityCreate, EntityUpdate
from workouts.models.generic.safe_entity import SafeEntity


@dataclass
class WorkoutCreate(EntityCreate):
    user: User
    name: str
    date: datetime


class WorkoutUpdate(EntityUpdate):
    pass


class Workout(SafeEntity):
    date: Field = models.DateField(verbose_name="workout date")
    name: Field = CICharField(max_length=150)
    user: Field = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.date} - {self.name}"

    class Meta:
        app_label = "workouts"
        unique_together = ["name", "date"]
        indexes = [models.Index(fields=["user"])]
