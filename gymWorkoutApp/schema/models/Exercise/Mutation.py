import graphene
from .Type import ExerciseType
from gymWorkoutApp.models import Exercise

# Группы мышц
class MuscleGroup(graphene.Enum):
    LEGS = 'legs'
    HANDS = 'hands'
    BACK = 'back'
    SHOULDERS = 'shoulders'
    CHEST = 'chest'

# Создает новое упражнение
class CreateExercise(graphene.Mutation):
  class Arguments:
    title = graphene.String()
    description = graphene.String()
    training_apparatus = graphene.ID()
    muscle_group = MuscleGroup()

  exercise = graphene.Field(ExerciseType)

  def mutate(
      self,
      info,
      title,
      description,
      training_apparatus,
      muscle_group
    ):
    exercise = Exercise.objects.create(
      title = title,
      description = description,
      muscle_group = muscle_group,
      training_apparatus = TrainingApparatus.objects.get(pk=training_apparatus)
    )

    exercise.save()

    return CreateExercise(
      exercise=exercise
    )

# Обновляет упражение
class UpdateExercise(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    training_apparatus = graphene.ID()
    muscle_group = MuscleGroup()

  exercise = graphene.Field(ExerciseType)

  def mutate(
      self,
      info,
      id,
      title=None,
      description=None,
      training_apparatus=None,
      muscle_group=None
    ):
    exercise = Exercise.objects.get(pk=id)

    exercise.title = title if title is not None else exercise.title
    exercise.description = description if description is not None else exercise.description
    exercise.training_apparatus = TrainingApparatus.objects.get(pk=training_apparatus) if training_apparatus is not None else exercise.training_apparatus
    exercise.muscle_group = muscle_group if muscle_group is not None else exercise.muscle_group

    exercise.save()

    return UpdateExercise(
      exercise=exercise
    )

# Удаляет упражнение
class DeleteExercise(graphene.Mutation):
  class Arguments:
    id = graphene.ID()

  ok = graphene.Boolean()

  def mutate(
      self,
      info,
      id
    ):
    try:
      exercise = Exercise.objects.get(pk=id)

      if exercise is not None:
          exercise.delete()
          return DeleteExercise(ok=True)
    except:
        return DeleteExercise(ok=False)

    return DeleteExercise(ok=False)


class ExerciseMutation(graphene.ObjectType):
    create_exercise = CreateExercise.Field()
    update_exercise = UpdateExercise.Field()
    delete_exercise = DeleteExercise.Field()
