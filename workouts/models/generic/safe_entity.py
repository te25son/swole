from django.db import models
from django.db.models.fields import Field
from django.utils import timezone
from returns.maybe import Maybe

from workouts.models.generic.entity import Entity


class SafeEntityQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class SafeEntityManager(models.Manager):
    def __init__(self, alive_only: bool | None = None, *args, **kwargs) -> None:
        self.alive_only = Maybe.from_optional(alive_only).value_or(True)
        super().__init__(*args, **kwargs)

    def get_queryset(self) -> SafeEntityQuerySet:
        if self.alive_only:
            return SafeEntityQuerySet(self.model).filter(deleted_at=None)
        return SafeEntityQuerySet(self.model)

    def delete(self):
        return self.get_queryset().delete()

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SafeEntity(Entity):
    deleted_at: Field = models.DateTimeField(blank=True, null=True)

    objects: SafeEntityManager = SafeEntityManager(alive_only=True)
    all_objects: SafeEntityManager = SafeEntityManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()
