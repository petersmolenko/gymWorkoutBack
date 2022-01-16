import graphene
from .Type import TrainingApparatusType
from gymWorkoutApp.models import TrainingApparatus

class TrainerQuery(graphene.ObjectType):
    trainers = graphene.List(TrainingApparatusType)
    trainer = graphene.Field(TrainingApparatusType, id=graphene.ID())

    # Получаем все тренажеры
    def resolve_trainers(self, info, **kwargs):
        return TrainingApparatus.objects.all()

    # Получаем тренажер по ID
    def resolve_trainer(self, info, id):
        return TrainingApparatus.objects.get(pk=id)
