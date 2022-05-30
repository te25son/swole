from django.db import models
from django.utils import timezone
from returns.maybe import Maybe


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
