import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_http_methods

from utils.decorators import (
    exercise_create_action,
    no_direct_url_access,
    workout_action,
)
from utils.response_context import Context
from utils.view_helper import render_view
from workouts.forms import CreateNewExerciseForm
from workouts.logic.exercise_logic import ExerciseRepository
from workouts.models import Exercise, Workout
from workouts.models.exercise import ExerciseCreate

Exercises = ExerciseRepository()


@require_GET
@login_required
@no_direct_url_access
@workout_action
def exercise_get_all(
    request: HttpRequest, workout: Workout, context: Context
) -> HttpResponse:
    context["exercises"] = Exercises.get_all_by_workout(workout.id)
    return render_view(request, context)


@require_http_methods(["GET", "POST"])
@login_required
@no_direct_url_access
@exercise_create_action
def exercise_create(
    request: HttpRequest, workout: Workout, is_new_exercise: bool, context: Context
) -> HttpResponse:
    if is_new_exercise:
        return _create_new_exercise(request, workout, context)
    return _create_from_existing(request, workout, context)


def _create_new_exercise(
    request: HttpRequest, workout: Workout, context: Context
) -> HttpResponse:
    if request.method == "POST":
        form = CreateNewExerciseForm(data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            exercise = Exercises.create(
                ExerciseCreate(name=form.data["name"], workouts=[workout])
            )
            context["exercise"] = exercise

            return render_view(
                request=request, context=context, trigger="update_exercises"
            )
        else:
            context["form"] = form

            return render_view(request, context)

    context["form"] = CreateNewExerciseForm()

    return render_view(request, context)


def _create_from_existing(
    request: HttpRequest, workout: Workout, context: Context
) -> HttpResponse:
    if request.method == "POST":
        exercise_id = request.POST.get("exercise-id")
        exercise_id_as_uuid = uuid.UUID(exercise_id)
        exercise = get_object_or_404(klass=Exercise, pk=exercise_id_as_uuid)
        exercise.workouts.add(workout)
        exercise.save()

        context["exercise"] = exercise

        return render_view(request=request, context=context, trigger="update_exercises")

    context["exercises"] = Exercises.get_all_by_user(request.user)
    return render_view(request, context)
