from graphene_django import DjangoObjectType
from gymWorkoutApp.models import WorkoutPart

class WorkoutPartType(DjangoObjectType):
    class Meta:
        model = WorkoutPart
