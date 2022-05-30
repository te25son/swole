from django.forms import ModelForm

from workouts.models import Set


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ["rep_count", "weight"]
