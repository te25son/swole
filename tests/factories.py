import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from faker import Faker

from workouts.models import Exercise, Set, Workout

TEST_PASSWORD = "i8X2v81@27it5Zg"
FAKE = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda x: FAKE.unique.name())
    password = factory.LazyFunction(lambda: make_password(TEST_PASSWORD))

    class Meta:
        model = settings.AUTH_USER_MODEL


class WorkoutFactory(factory.django.DjangoModelFactory):
    date = factory.LazyAttribute(lambda x: now())
    name = factory.LazyAttribute(lambda x: FAKE.name())
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Workout


class ExerciseFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: FAKE.unique.name())

    class Meta:
        model = Exercise

    @factory.post_generation
    def workouts(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing
            return
        self.workouts.add(*extracted)


class SetFactory(factory.django.DjangoModelFactory):
    workout = factory.SubFactory(WorkoutFactory)
    exercise = factory.SubFactory(ExerciseFactory)
    weight = factory.LazyAttribute(lambda x: FAKE.random_int(1, 2000))
    rep_count = factory.LazyAttribute(lambda x: FAKE.random_int(1, 50))

    class Meta:
        model = Set
