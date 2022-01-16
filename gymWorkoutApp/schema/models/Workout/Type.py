from graphene_django import DjangoObjectType
from gymWorkoutApp.models import Workout

class WorkoutType(DjangoObjectType):
    class Meta:
        model = Workout
