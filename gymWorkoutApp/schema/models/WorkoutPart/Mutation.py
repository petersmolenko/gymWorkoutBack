import graphene
from .Type import WorkoutPartType
from gymWorkoutApp.models import WorkoutPart

# Служит для удаления сущностей выбранной модели по их ID
def deleteItemsOf(model, ids):
    for i in range(len(ids)):
      workoutPart = model.objects.get(pk=ids[i])

      if workoutPart is not None:
          workoutPart.delete()

# Создает новый этап тренировки
class CreateWorkoutPart(graphene.Mutation):
  class Arguments:
    title = graphene.String()
    description = graphene.String()
    exercise = graphene.ID()
    weight = graphene.Float()
    repetitions_number = graphene.Int()
    sort_order = graphene.Int()
    completed = graphene.Boolean()

  workoutPart = graphene.Field(WorkoutPartType)

  def mutate(
      self,
      info,
      title,
      description,
      exercise,
      weight=0,
      repetitions_number=0,
      sort_order=0,
      completed=False,
    ):
    workoutPart = WorkoutPart.objects.create(
      title = title,
      description = description,
      weight = weight,
      repetitions_number = repetitions_number,
      sort_order = sort_order,
      completed = completed,
      exercise = Exercise.objects.get(pk=exercise)
    )

    workoutPart.save()

    return CreateWorkoutPart(
      workoutPart=workoutPart
    )

# Обновляет этап тренировки
class UpdateWorkoutPart(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    exercise = graphene.ID()
    weight = graphene.Float()
    repetitions_number = graphene.Int()
    sort_order = graphene.Int()
    completed = graphene.Boolean()

  workoutPart = graphene.Field(WorkoutPartType)

  def mutate(
      self,
      info,
      id,
      title=None,
      description=None,
      exercise=None,
      weight=None,
      repetitions_number=None,
      sort_order=None,
      completed=False,
    ):
    workoutPart = WorkoutPart.objects.get(pk=id)

    workoutPart.title = title if title is not None else workoutPart.title
    workoutPart.description = description if description is not None else workoutPart.description
    workoutPart.exercise = Exercise.objects.get(pk=exercise) if exercise is not None else workoutPart.exercise
    workoutPart.weight = weight if weight is not None else workoutPart.weight
    workoutPart.repetitions_number = repetitions_number if repetitions_number is not None else workoutPart.repetitions_number
    workoutPart.sort_order = sort_order if sort_order is not None else workoutPart.sort_order
    workoutPart.completed = completed if completed is not None else workoutPart.completed

    workoutPart.save()

    return UpdateWorkoutPart(
      workoutPart=workoutPart
    )

# Удаляет сущности WorkoutParts (этап тренировки) по их ID
class DeleteWorkoutParts(graphene.Mutation):
  class Arguments:
    ids = graphene.List(graphene.ID)

  ids = graphene.List(graphene.ID)

  def mutate(self, info, ids=[]):
    try:
      deleteItemsOf(WorkoutPart, ids)
      #
      return DeleteWorkoutParts(ids=ids)
    except:
      return DeleteWorkoutParts(ids=[])

    return DeleteWorkoutParts(ids=ids)

class WorkoutPartsMutation(graphene.ObjectType):
    create_workout_part = CreateWorkoutPart.Field()
    update_workout_part = UpdateWorkoutPart.Field()
    delete_workout_parts = DeleteWorkoutParts.Field()
