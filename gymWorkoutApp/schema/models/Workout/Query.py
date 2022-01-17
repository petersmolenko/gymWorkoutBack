import graphene
from ..WorkoutPart.Type import WorkoutPartType
from .Type import WorkoutType
from gymWorkoutApp.models import Workout

class WorkoutQuery(graphene.ObjectType):
    workouts = graphene.List(WorkoutType)
    completed_workouts = graphene.List(WorkoutType)
    active_workouts = graphene.Field(WorkoutType)
    workout = graphene.Field(WorkoutType, id=graphene.ID())

    # Получаем все тренировки
    def resolve_workouts(self, info, **kwargs):
        return Workout.objects.all()

    # Получаем все активные тренировки
    def resolve_active_workouts(self, info, **kwargs):
        return Workout.objects.get(in_process=True)

    # Получаем все завершенные тренировки
    def resolve_completed_workouts(self, info, **kwargs):
        return Workout.objects.filter(completed=True)

    # Получаем тренировку по id
    def resolve_workout(self, info, id):
        return Workout.objects.get(pk=id)
