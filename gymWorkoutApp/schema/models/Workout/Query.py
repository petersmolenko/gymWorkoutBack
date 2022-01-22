import graphene
from ..WorkoutPart.Type import WorkoutPartType
from .Type import WorkoutType
from gymWorkoutApp.models import Workout

class WorkoutQuery(graphene.ObjectType):
    workouts = graphene.List(WorkoutType)
    completed_workouts = graphene.List(WorkoutType)
    active_workout = graphene.Field(WorkoutType)
    workout = graphene.Field(WorkoutType, id=graphene.ID())

    # Получаем все тренировки
    def resolve_workouts(self, info, **kwargs):
        return Workout.objects.all()

    # Получаем все активную тренировку
    def resolve_active_workout(self, info, **kwargs):
        workout = None
        try:
            workout = Workout.objects.get(status="a")
        except:
            pass

        return workout

    # Получаем все завершенные тренировки
    def resolve_completed_workouts(self, info, **kwargs):
        return Workout.objects.filter(completed=True)

    # Получаем тренировку по id
    def resolve_workout(self, info, id):
        return Workout.objects.get(pk=id)
