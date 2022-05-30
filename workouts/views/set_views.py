from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from utils.decorators import (
    no_direct_url_access,
    workout_exercise_action,
    workout_exercise_set_action,
)
from utils.response_context import Context
from utils.view_helper import HtmxResponse, render_view
from workouts.forms import SetForm
from workouts.logic.set_repository import SetRepository
from workouts.models import Exercise, Set, SetCreate, Workout

Sets = SetRepository()


@require_GET
@login_required
@no_direct_url_access
@workout_exercise_set_action
def set_get(
    request: HttpRequest,
    workout: Workout,
    exercise: Exercise,
    set: Set,
    context: Context,
) -> HttpResponse:
    return render_view(request, context)


@require_GET
@login_required
@no_direct_url_access
@workout_exercise_action
def set_get_all(
    request: HttpRequest, workout: Workout, exercise: Exercise, context: Context
) -> HttpResponse:
    context["sets"] = Sets.get_all_by_workout_and_exercise(workout.id, exercise.id)
    return render_view(request, context)


@require_http_methods(["GET", "POST"])
@login_required
@no_direct_url_access
@workout_exercise_action
def set_create(
    request: HttpRequest, workout: Workout, exercise: Exercise, context: Context
) -> HttpResponse:
    if request.method == "POST":
        if workout not in exercise.workouts.all():
            pass

        form = SetForm(data=request.POST)
        context["form"] = form

        if form.is_valid():
            form.save(commit=False)
            Sets.create(
                SetCreate(
                    workout=workout,
                    exercise=exercise,
                    weight=form.cleaned_data["weight"],
                    rep_count=form.cleaned_data["rep_count"],
                )
            )
            return HtmxResponse(trigger=f"update_sets_{exercise.id}")

        return render_view(request, context)

    return render_view(request, context)


@require_http_methods(["GET", "POST"])
@login_required
@no_direct_url_access
@workout_exercise_set_action
def set_update(
    request: HttpRequest,
    workout: Workout,
    exercise: Exercise,
    set: Set,
    context: Context,
) -> HttpResponse:
    if request.method == "POST":
        form = SetForm(request.POST, instance=set)

        if form.is_valid():
            form.save()
            return render_view(
                request, context, template_override="workouts/set_get.html"
            )

        context["form"] = form
        return render_view(request, context)

    return render_view(request, context)


@require_POST
@login_required
@no_direct_url_access
@workout_exercise_set_action
def set_delete(
    request: HttpRequest,
    workout: Workout,
    exercise: Exercise,
    set: Set,
    context: Context,
) -> HttpResponse:
    Sets.delete(set)

    return HtmxResponse(trigger=f"delete_set_from_{exercise.id}")
