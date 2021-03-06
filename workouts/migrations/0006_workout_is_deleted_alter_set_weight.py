# Generated by Django 4.0.4 on 2022-05-04 05:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workouts", "0005_alter_set_weight_alter_workout_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="workout",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="set",
            name="weight",
            field=models.PositiveSmallIntegerField(
                default=0,
                validators=[
                    django.core.validators.MaxValueValidator(
                        2000, message="Weight cannot be greater than 2000."
                    )
                ],
            ),
        ),
    ]
