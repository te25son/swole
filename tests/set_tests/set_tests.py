from typing import Callable
from uuid import UUID

import faker
import pytest
from django.http import HttpResponse

from tests.conftest import RequestMethod
from workouts.logic.set_repository import SetRepository
from workouts.models import Exercise, Set, SetCreate, Workout

fake = faker.Faker()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, method",
    [
        ("workouts:set_get_all", RequestMethod.GET),
        ("workouts:set_create", RequestMethod.GET),
        ("workouts:set_create", RequestMethod.POST),
        ("workouts:set_get", RequestMethod.GET),
        ("workouts:set_update", RequestMethod.GET),
        ("workouts:set_update", RequestMethod.POST),
        ("workouts:set_delete", RequestMethod.POST),
    ],
)
def test_set_views_require_login(
    workout: Workout,
    exercise: Exercise,
    set: Set,
    view_name: str,
    method: RequestMethod,
    response_factory: Callable[..., HttpResponse],
) -> None:
    data = _get_set_request_data(workout.id, exercise.id, set.id, view_name)
    response = response_factory(method, view_name, kwargs=data)

    assert response.status_code == 302
    assert "/users/login/" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, method",
    [
        ("workouts:set_get_all", RequestMethod.GET),
        ("workouts:set_create", RequestMethod.GET),
        ("workouts:set_create", RequestMethod.POST),
        ("workouts:set_get", RequestMethod.GET),
        ("workouts:set_update", RequestMethod.GET),
        ("workouts:set_update", RequestMethod.POST),
        ("workouts:set_delete", RequestMethod.POST),
    ],
)
def test_set_views_dont_allow_direct_access(
    workout_with_signed_in_user: Workout,
    exercise: Exercise,
    set: Set,
    view_name: str,
    method: RequestMethod,
    response_factory: Callable[..., HttpResponse],
) -> None:
    data = _get_set_request_data(
        workout_with_signed_in_user.id, exercise.id, set.id, view_name
    )
    response = response_factory(method, view_name, kwargs=data)

    assert response.status_code == 404


@pytest.mark.django_db
def test_can_create_set(
    workout: Workout, exercise: Exercise, set_repo: SetRepository
) -> None:
    weight = 100
    rep_count = 10
    set = set_repo.create(SetCreate(workout, exercise, weight, rep_count))

    assert set.workout == workout
    assert set.exercise == exercise
    assert set.weight == weight
    assert set.rep_count == rep_count
    assert set.name == "Set 1"


@pytest.mark.django_db
def test_set_naming(
    workout: Workout, exercise: Exercise, set_repo: SetRepository
) -> None:
    for _ in range(20):
        set_repo.create(
            SetCreate(
                workout=workout,
                exercise=exercise,
                weight=fake.unique.random_int(min=1, max=100),
                rep_count=fake.unique.random_int(min=1, max=100),
            )
        )

    sets = list(
        Set.objects.filter(workout__id=workout.id, exercise__id=exercise.id).all()
    )

    for index, set in enumerate(sets, start=1):
        assert set.name == f"Set {index}"


def _get_set_request_data(
    workout_id: UUID, exercise_id: UUID, set_id: UUID, view_name: str
) -> dict[str, UUID]:
    data = {"workout_id": workout_id, "exercise_id": exercise_id}

    match view_name:
        case "workouts:set_get" | "workouts:set_update" | "workouts:set_delete":
            data.update({"set_id": set_id})

    return data
