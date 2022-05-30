from django.urls import path

from . import views

app_name = "workouts"
urlpatterns = [
    path("", views.home, name="home"),
    path("workouts/", views.workout_get_all, name="workout_get_all"),
    path("workouts/create/", views.workout_create, name="workout_create"),
    path("workouts/<uuid:id>/", views.workout_detail, name="workout_detail"),
    path("workouts/<uuid:id>/delete/", views.workout_delete, name="workout_delete"),
    path(
        "workouts/<uuid:id>/exercises/", views.exercise_get_all, name="exercise_get_all"
    ),
    path(
        "workouts/<uuid:id>/exercises/create/<int:is_new>/",
        views.exercise_create,
        name="exercise_create",
    ),
    path(
        "workouts/<uuid:workout_id>/exercises/<uuid:exercise_id>/sets/",
        views.set_get_all,
        name="set_get_all",
    ),
    path(
        "workouts/<uuid:workout_id>/exercises/<uuid:exercise_id>/sets/create/",
        views.set_create,
        name="set_create",
    ),
    path(
        "workouts/<uuid:workout_id>/exercises/<uuid:exercise_id>/sets/<uuid:set_id>/get/",
        views.set_get,
        name="set_get",
    ),
    path(
        "workouts/<uuid:workout_id>/exercises/<uuid:exercise_id>/sets/<uuid:set_id>/update/",
        views.set_update,
        name="set_update",
    ),
    path(
        "workouts/<uuid:workout_id>/exercises/<uuid:exercise_id>/sets/<uuid:set_id>/delete/",
        views.set_delete,
        name="set_delete",
    ),
]
