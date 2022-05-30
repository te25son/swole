from enum import Enum
from typing import Any, Callable, Dict, Optional

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_factoryboy import register
from returns.maybe import Maybe

from tests.factories import ExerciseFactory, SetFactory, UserFactory, WorkoutFactory
from users.models import User
from workouts.logic.set_repository import SetRepository
from workouts.models.workout import Workout

register(UserFactory)
register(WorkoutFactory)
register(ExerciseFactory)
register(SetFactory)


class RequestMethod(Enum):
    GET = 1
    POST = 2


@pytest.fixture(scope="session")
def client():
    return Client()


# RESPONSES
@pytest.fixture
def get_response_factory(db, client: Client) -> Callable:
    def response(viewname: Optional[str] = None, *args, **kwargs):
        view = Maybe.from_optional(viewname).value_or("account_login")
        return client.get(reverse(view, *args, **kwargs))

    return response


@pytest.fixture
def post_response_factory(db, client: Client) -> Callable:
    def response(viewname, form_data: Optional[Dict] = None, *args, **kwargs):
        url = reverse(viewname, *args, **kwargs)
        return client.post(url, data=form_data)

    return response


@pytest.fixture
def response_factory(db, client: Client) -> Callable[..., HttpResponse]:
    def response(
        method: RequestMethod,
        view_name: str,
        form_data: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs
    ):
        match method:
            case RequestMethod.GET:
                return client.get(reverse(view_name, *args, **kwargs))
            case RequestMethod.POST:
                url = reverse(view_name, *args, **kwargs)
                return client.post(url, data=form_data)

    return response


# USERS
@pytest.fixture
def signed_in_user(client: Client, user: User) -> User:
    client.force_login(user)
    return user


@pytest.fixture
def workout_with_signed_in_user(client: Client, workout: Workout) -> Workout:
    client.force_login(workout.user)
    return workout


# REPOSITORIES
@pytest.fixture
def set_repo() -> SetRepository:
    return SetRepository()
