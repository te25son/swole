from django import forms

from workouts.models import Exercise


class CreateNewExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name"]
