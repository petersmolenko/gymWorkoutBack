import graphene
from .Type import WorkoutPartType
from gymWorkoutApp.models import WorkoutPart, Workout

class WorkoutPartsQuery(graphene.ObjectType):
    workout_parts = graphene.List(WorkoutPartType)
    workout_parts_by_workout = graphene.List(WorkoutPartType, id=graphene.ID())

    # Получаем все этапы тренировок
    def resolve_workout_parts(self, info, **kwargs):
        return WorkoutPart.objects.all()

    # Получаем этапы тренировок для конкретной тренировки
    def resolve_workout_parts_by_workout(self, info, id):
        return Workout.objects.get(pk=id).workout_parts.all()
