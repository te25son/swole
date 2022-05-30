from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from utils.decorators import no_direct_url_access, non_entity_action, workout_action
from utils.response_context import Context, WorkoutsContext
from utils.view_helper import HtmxResponse, render_view
from workouts.forms import WorkoutCreateForm
from workouts.logic.exercise_logic import user_has_existing_exercises
from workouts.logic.workout_repository import WorkoutRepository
from workouts.models import Workout, WorkoutCreate

Workouts = WorkoutRepository()


@require_GET
@login_required
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")



@require_GET
@login_required
@non_entity_action(WorkoutsContext)
def workout_get_all(request: HttpRequest, context: WorkoutsContext) -> HttpResponse:
    context["workouts"] = Workouts.get_all_by_user(request.user)
    return render_view(request, context)


@require_http_methods(["GET", "POST"])
@login_required
@no_direct_url_access
@non_entity_action(WorkoutsContext)
def workout_create(request: HttpRequest, context: WorkoutsContext) -> HttpResponse:
    if request.method == "POST":
        form = WorkoutCreateForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            Workouts.create(
                WorkoutCreate(
                    user=request.user,
                    name=form.cleaned_data["name"],
                    date=form.cleaned_data["date"],
                )
            )

            return HtmxResponse(trigger="workout_created")

        context["form"] = form
        return render_view(request, context)

    context["form"] = WorkoutCreateForm()
    return render_view(request, context)


@require_GET
@login_required
@workout_action
def workout_detail(
    request: HttpRequest, workout: Workout, context: Context
) -> HttpResponse:
    # this should probably be a property in the user model
    context["has_exercises"] = user_has_existing_exercises(request.user)
    return render_view(request, context)


@require_POST
@login_required
@no_direct_url_access
@workout_action
def workout_delete(
    request: HttpRequest, workout: Workout, context: Context
) -> HttpResponse:
    workout.delete()

    return HtmxResponse(trigger="workout_deleted")
