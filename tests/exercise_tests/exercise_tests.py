from typing import Any, Callable, Dict, Optional
from uuid import UUID

import faker
import pytest
from django.http import HttpResponse

from tests.conftest import RequestMethod
from workouts.forms import CreateNewExerciseForm
from workouts.forms.exercise_forms import CreateNewExerciseForm
from workouts.models import Exercise, Workout

fake = faker.Faker()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, is_new_option, method",
    [
        ("workouts:exercise_get_all", None, RequestMethod.GET),
        ("workouts:exercise_create", 0, RequestMethod.GET),
        ("workouts:exercise_create", 1, RequestMethod.GET),
        ("workouts:exercise_create", 0, RequestMethod.POST),
        ("workouts:exercise_create", 1, RequestMethod.POST),
    ],
)
def test_exercise_views_require_login(
    workout: Workout,
    view_name: str,
    method: RequestMethod,
    is_new_option: Optional[int],
    response_factory: Callable[..., HttpResponse],
) -> None:
    data = _get_exercise_view_data(workout.id, is_new_option)
    response = response_factory(method, view_name, kwargs=data)

    assert response.status_code == 302
    assert "/users/login/" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, is_new_option, method",
    [
        ("workouts:exercise_get_all", None, RequestMethod.GET),
        ("workouts:exercise_create", 0, RequestMethod.GET),
        ("workouts:exercise_create", 1, RequestMethod.GET),
        ("workouts:exercise_create", 0, RequestMethod.POST),
        ("workouts:exercise_create", 1, RequestMethod.POST),
    ],
)
def test_exercise_views_dont_allow_direct_access(
    workout_with_signed_in_user: Workout,
    view_name: str,
    method: RequestMethod,
    is_new_option: Optional[int],
    response_factory: Callable[..., HttpResponse],
) -> None:
    data = _get_exercise_view_data(workout_with_signed_in_user.id, is_new_option)
    response = response_factory(method, view_name, kwargs=data)

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, is_new_option, method",
    [
        ("workouts:exercise_get_all", None, RequestMethod.GET),
        ("workouts:exercise_create", 0, RequestMethod.GET),
        ("workouts:exercise_create", 1, RequestMethod.GET),
        ("workouts:exercise_create", 0, RequestMethod.POST),
        ("workouts:exercise_create", 1, RequestMethod.POST),
    ],
)
def test_exercise_views_succeed(
    workout_with_signed_in_user: Workout,
    view_name: str,
    is_new_option: Optional[int],
    method: str,
    response_factory: Callable[..., HttpResponse],
) -> None:
    data = _get_exercise_view_data(workout_with_signed_in_user.id, is_new_option)
    response_factory(method, view_name, kwargs=data)
    response = response_factory(
        method=RequestMethod.GET,
        view_name="workouts:workout_detail",
        kwargs={"id": workout_with_signed_in_user.id},
    )

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_new, use_empty_data, should_succeed",
    [(0, False, False), (1, False, True), (0, True, False), (1, True, False)],
)
def test_exercise_create_form(
    exercise: Exercise, is_new: int, use_empty_data: bool, should_succeed: bool
) -> None:
    form_data = (
        {}
        if use_empty_data
        else {"name": fake.name() if is_new == 1 else exercise.name}
    )
    form = CreateNewExerciseForm(data=form_data)

    assert form.is_valid() == should_succeed


def _get_exercise_view_data(
    workout_id: UUID, is_new_option: Optional[int]
) -> Dict[str, Any]:
    data: Dict[str, Any] = {"id": workout_id}

    if is_new_option is not None:
        data.update({"is_new": is_new_option})

    return data
