import uuid

from django.db import models
from django.db.models.fields import Field
from django.utils import timezone

from .safe import SafeEntityManager


class EntityCreate:
    pass


class EntityUpdate:
    pass


class Entity(models.Model):
    id: Field = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


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
