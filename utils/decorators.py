from functools import wraps
from typing import Callable, Type, TypeVar
from uuid import UUID

from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from workouts.models import Exercise, Set, Workout

from .response_context import AccountContext, WorkoutsContext

_TContext = TypeVar("_TContext", WorkoutsContext, AccountContext)


def no_direct_url_access(
    func: Callable[..., HttpResponse]
) -> Callable[..., HttpResponse]:
    @wraps(func)
    def inner(request: HttpRequest, *args, **kwargs):
        referer = request.META.get("HTTP_REFERER")
        if not referer:
            raise Http404()
        return func(request, *args, **kwargs)

    return inner


def non_entity_action(context_type: Type[_TContext]) -> Callable[..., HttpResponse]:
    def inner(func: Callable[..., HttpResponse]):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            return func(
                request,
                context=context_type(
                    template_name=func.__name__,
                    hx_request_header=request.META.get("HTTP_HX_REQUEST"),
                ),
                *args,
                **kwargs
            )

        return wrapper

    return inner


def entity_action(
    func: Callable[..., HttpResponse], klass: Type
) -> Callable[..., HttpResponse]:
    @wraps(func)
    def wrapper(request: HttpRequest, id: UUID, *args, **kwargs):
        entity = get_object_or_404(klass=klass, pk=id)

        if isinstance(entity, Workout) and not entity.user == request.user:
            return HttpResponseForbidden(request)

        return func(
            request,
            entity,
            context=WorkoutsContext(
                template_name=func.__name__,
                hx_request_header=request.META.get("HTTP_HX_REQUEST"),
                data={type(entity).__name__.lower(): entity},
            ),
            *args,
            **kwargs
        )

    return wrapper


def workout_action(func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    return entity_action(func, Workout)


def exercise_action(func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    return entity_action(func, Exercise)


def exercise_create_action(
    func: Callable[..., HttpResponse]
) -> Callable[..., HttpResponse]:
    @wraps(func)
    def wrapper(request: HttpRequest, id: UUID, is_new: int):
        workout = get_object_or_404(klass=Workout, pk=id)

        if not workout.user == request.user:
            return HttpResponseForbidden()

        is_new_exercise = True if is_new == 1 else False
        return func(
            request,
            workout,
            is_new_exercise,
            context=WorkoutsContext(
                template_name=func.__name__,
                hx_request_header=request.META.get("HTTP_HX_REQUEST"),
                data={"workout": workout, "is_new": is_new},
            ),
        )

    return wrapper


def workout_exercise_action(
    func: Callable[..., HttpResponse]
) -> Callable[..., HttpResponse]:
    @wraps(func)
    def wrapper(
        request: HttpRequest, workout_id: UUID, exercise_id: UUID, *args, **kwargs
    ):
        workout = get_object_or_404(klass=Workout, pk=workout_id)
        exercise = get_object_or_404(klass=Exercise, pk=exercise_id)

        if not workout.user == request.user:
            return HttpResponseForbidden()

        return func(
            request,
            workout,
            exercise,
            context=WorkoutsContext(
                template_name=func.__name__,
                hx_request_header=request.META.get("HTTP_HX_REQUEST"),
                data={"workout": workout, "exercise": exercise},
            ),
            *args,
            **kwargs
        )

    return wrapper


def workout_exercise_set_action(
    func: Callable[..., HttpResponse]
) -> Callable[..., HttpResponse]:
    @wraps(func)
    def wrapper(
        request: HttpRequest,
        workout_id: UUID,
        exercise_id: UUID,
        set_id: UUID,
        *args,
        **kwargs
    ):
        workout = get_object_or_404(klass=Workout, pk=workout_id)
        exercise = get_object_or_404(klass=Exercise, pk=exercise_id)
        set = get_object_or_404(klass=Set, pk=set_id)

        if not workout.user == request.user:
            return HttpResponseForbidden()

        return func(
            request,
            workout,
            exercise,
            set,
            context=WorkoutsContext(
                template_name=func.__name__,
                hx_request_header=request.META.get("HTTP_HX_REQUEST"),
                data={"workout": workout, "exercise": exercise, "set": set},
            ),
            *args,
            **kwargs
        )

    return wrapper
