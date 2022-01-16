import graphene
from .Type import ExerciseType
from gymWorkoutApp.models import Exercise

class ExerciseQuery(graphene.ObjectType):
    exercises = graphene.List(ExerciseType)
    exercise = graphene.Field(ExerciseType, id=graphene.ID())

    # Получаем все упражнения
    def resolve_exercises(self, info, **kwargs):
        return Exercise.objects.all()

    # Получаем упражнение по id
    def resolve_exercise(self, info, id):
        return Exercise.objects.get(pk=id)
