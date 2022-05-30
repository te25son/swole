from datetime import timedelta
from typing import Callable

import faker
import pytest
from django.http import HttpResponse
from django.utils import timezone
from psycopg2 import IntegrityError
from pytest_django.asserts import assertContains, assertNotContains

from tests.conftest import RequestMethod
from tests.factories import WorkoutFactory
from users.models import User
from workouts.forms import WorkoutCreateForm
from workouts.models import Exercise, Workout
from workouts.logic.workout_repository import WorkoutRepository

fake = faker.Faker()


@pytest.fixture
def workout_repo() -> WorkoutRepository:
    return WorkoutRepository()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, method",
    [
        ("workouts:home", RequestMethod.GET),
        ("workouts:workout_get_all", RequestMethod.GET),
        ("workouts:workout_detail", RequestMethod.GET),
        ("workouts:workout_create", RequestMethod.GET),
        ("workouts:workout_create", RequestMethod.POST),
    ],
)
def test_workout_views_require_login(
    workout: Workout,
    view_name: str,
    method: RequestMethod,
    response_factory: Callable[..., HttpResponse],
) -> None:
    data = {"id": workout.id} if view_name == "workouts:workout_detail" else {}
    response = response_factory(method, view_name, kwargs=data)

    assert response.status_code == 302
    assert "/users/login/" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, method, expected_status_code",
    [
        ("workouts:home", RequestMethod.GET, 200),
        ("workouts:workout_get_all", RequestMethod.GET, 200),
        ("workouts:workout_detail", RequestMethod.GET, 200),
        ("workouts:workout_create", RequestMethod.GET, 404),
        ("workouts:workout_create", RequestMethod.POST, 404),
    ],
)
def test_workout_views_direct_access(
    workout_with_signed_in_user: Workout,
    view_name: str,
    method: RequestMethod,
    expected_status_code: int,
    response_factory: Callable[..., HttpResponse],
) -> None:
    data = (
        {"id": workout_with_signed_in_user.id}
        if view_name == "workouts:workout_detail"
        else {}
    )
    response = response_factory(method, view_name, kwargs=data)

    assert response.status_code == expected_status_code


@pytest.mark.django_db
def test_workout_get_all_page_only_displays_signed_in_users_workouts(
    workout_with_signed_in_user: Workout,
    workout_factory: WorkoutFactory,
    response_factory: Callable[..., HttpResponse],
) -> None:
    workout_not_belonging_to_signed_in_user = workout_factory()
    response = response_factory(RequestMethod.GET, "workouts:workout_get_all")

    assert (
        workout_with_signed_in_user.user != workout_not_belonging_to_signed_in_user.user
    )
    assertContains(response, workout_with_signed_in_user.name)
    assertNotContains(response, workout_not_belonging_to_signed_in_user.name)


@pytest.mark.django_db
def test_workout_detail_page_contains_correct_content(
    workout_with_signed_in_user: Workout,
    exercise: Exercise,
    response_factory: Callable[..., HttpResponse],
) -> None:
    exercise.workouts.add(workout_with_signed_in_user)

    formatted_workout_date = workout_with_signed_in_user.date.strftime("%b %d %Y")
    response = response_factory(
        method=RequestMethod.GET,
        view_name="workouts:workout_detail",
        kwargs={"id": workout_with_signed_in_user.id},
    )

    assert workout_with_signed_in_user in exercise.workouts.all()
    assertContains(
        response, f"{workout_with_signed_in_user.name} - {formatted_workout_date}"
    )
    assertContains(
        response, f'hx-get="/workouts/{workout_with_signed_in_user.id}/exercises/"'
    )
    assertContains(
        response,
        f'hx-get="/workouts/{workout_with_signed_in_user.id}/exercises/create/1/"',
    )
    assertContains(
        response,
        f'hx-get="/workouts/{workout_with_signed_in_user.id}/exercises/create/0/"',
    )
    assertContains(response, "Add exercise")
    assertContains(response, "Add new")
    assertContains(response, "From existing")


@pytest.mark.django_db
def test_can_create_new_workout(user: User, workout_factory: WorkoutFactory) -> None:
    date = fake.date_time(timezone.utc)
    name = fake.name()
    workout = workout_factory(date=date, user=user, name=name)

    assert workout.name == name
    assert workout.user == user
    assert workout.date == date


@pytest.mark.django_db
@pytest.mark.parametrize(
    "first_name, second_name", [("test", "Test"), ("TEST", "test"), ("TEST", "Test")]
)
def test_cannot_create_new_workout_with_same_name_and_date_case_insensitive(
    user: User, workout_factory: WorkoutFactory, first_name: str, second_name: str
) -> None:
    with pytest.raises(Exception) as error:
        date_1 = fake.date_time(timezone.utc)
        date_2 = date_1 + timedelta(seconds=1)

        workout_factory(date=date_1, user=user, name=first_name)
        workout_factory(date=date_2, user=user, name=second_name)

        assert isinstance(error, IntegrityError)


@pytest.mark.django_db
def test_can_create_workout_with_same_name_but_different_date(
    user: User, workout_factory: WorkoutFactory
) -> None:
    name = fake.name()
    date_1 = fake.date_time(timezone.utc)
    date_2 = date_1 + timedelta(days=1)
    workout_1 = workout_factory(date=date_1, user=user, name=name)
    workout_2 = workout_factory(date=date_2, user=user, name=name)

    assert date_1.date() != date_2.date()
    assert workout_1.name == name
    assert workout_1.user == user
    assert workout_1.date == date_1
    assert workout_2.name == name
    assert workout_2.user == user
    assert workout_2.date == date_2
    assert Workout.objects.filter(user__pk=user.pk).all().count() == 2


@pytest.mark.django_db
def test_can_create_workout_on_same_date_with_different_name(
    user: User, workout_factory: WorkoutFactory
) -> None:
    name_1 = fake.name()
    name_2 = fake.name()
    date_1 = fake.date_time(timezone.utc)
    date_2 = date_1 + timedelta(seconds=1)
    workout_1 = workout_factory(date=date_1, user=user, name=name_1)
    workout_2 = workout_factory(date=date_2, user=user, name=name_2)

    assert date_1.date() == date_2.date()
    assert workout_1.name == name_1
    assert workout_1.user == user
    assert workout_1.date == date_1
    assert workout_2.name == name_2
    assert workout_2.user == user
    assert workout_2.date == date_2
    assert Workout.objects.filter(user__pk=user.pk).all().count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize("use_empty_data", [True, False])
def test_workout_create_form(use_empty_data: bool) -> None:
    form_data = (
        {}
        if use_empty_data
        else {"name": fake.name(), "date": fake.date_time(timezone.utc)}
    )
    form = WorkoutCreateForm(form_data)

    assert form.is_valid() != use_empty_data


@pytest.mark.django_db
def test_workout_create_form_uses_custom_error(workout: Workout) -> None:
    form = WorkoutCreateForm({"name": workout.name, "date": workout.date})

    assert form.non_field_errors()[0] == "Workout name and date must be unique."


@pytest.mark.django_db
def test_workout_soft_delete(workout: Workout, workout_repo: WorkoutRepository) -> None:
    workout.delete()

    assert not workout.deleted_at == None
    assert len(workout_repo.get_all_by_user(workout.user, deleted=False)) == 0
    assert len(workout_repo.get_all_by_user(workout.user, deleted=True)) == 1


@pytest.mark.django_db
def test_workout_hard_delete(workout: Workout, workout_repo: WorkoutRepository) -> None:
    workout.hard_delete()

    assert len(workout_repo.get_all_by_user(workout.user, deleted=False)) == 0
    assert len(workout_repo.get_all_by_user(workout.user, deleted=True)) == 0
