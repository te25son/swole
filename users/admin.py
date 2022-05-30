from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "email",
        "username",
    ]


admin.site.register(User, UserAdmin)
