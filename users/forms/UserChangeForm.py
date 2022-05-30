from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )
