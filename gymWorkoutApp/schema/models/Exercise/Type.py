from graphene_django import DjangoObjectType
from gymWorkoutApp.models import Exercise

class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
