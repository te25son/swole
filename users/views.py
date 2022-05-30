from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from utils.decorators import non_entity_action
from utils.response_context import AccountContext
from utils.view_helper import render_view

from .forms import UserCreationForm


@require_http_methods(["GET", "POST"])
@non_entity_action(AccountContext)
def signup(request: HttpRequest, context: AccountContext) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("workouts:index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect("workouts:index")

        else:
            context.data.update({"form": form})

    else:
        context.data.update({"form": UserCreationForm()})

    return render_view(request, context)
