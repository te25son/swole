import uuid

from django.db import models
from django.db.models.fields import Field


class EntityCreate:
    pass


class EntityUpdate:
    pass


class Entity(models.Model):
    id: Field = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
