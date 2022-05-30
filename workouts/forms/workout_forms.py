from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from workouts.models import Workout


class DateInput(forms.DateInput):
    input_type = "date"


class WorkoutCreateForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data.get("name")
        cleaned_data.get("date")

        return cleaned_data

    class Meta:
        model = Workout
        fields = ["name", "date"]
        widgets = {"date": DateInput()}
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "Workout name and date must be unique."
            }
        }
