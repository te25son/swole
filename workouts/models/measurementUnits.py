from django.db import models
from django.utils.translation import gettext_lazy as _


class MeasurementUnits(models.TextChoices):
    KILOGRAMS = "KGS", _("Kilograms")
    POUNDS = "LBS", _("Pounds")
