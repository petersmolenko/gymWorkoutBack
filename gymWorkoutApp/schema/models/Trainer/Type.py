from graphene_django import DjangoObjectType
from gymWorkoutApp.models import TrainingApparatus

class TrainingApparatusType(DjangoObjectType):
    class Meta:
        model = TrainingApparatus
