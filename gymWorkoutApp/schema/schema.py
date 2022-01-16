# *
# Imports
# *

import graphene
from graphene_django import DjangoObjectType
from ..models import Workout, WorkoutPart, Exercise, TrainingApparatus, Profile
from .models.Trainer.Query import TrainerQuery
from .models.Trainer.Mutation import CreateTrainingApparatus, UpdateTrainingApparatus, DeleteTrainingApparatus
from .models.Workout.Query import WorkoutQuery
from .models.Workout.Mutation import CreateWorkout, UpdateWorkout, DeleteWorkout, AddWorkoutPartsToWorkout

# *
# Helpers
# *

# Служит для удаления сущностей выбранной модели по их ID
def deleteItemsOf(model, ids):
    for i in range(len(ids)):
      workoutPart = model.objects.get(pk=ids[i])

      if workoutPart is not None:
          workoutPart.delete()

class WorkoutPartType(DjangoObjectType):
    class Meta:
        model = WorkoutPart

class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class Query(
    TrainerQuery,
    WorkoutQuery,
    graphene.ObjectType
):
  # Profile queries
    profile = graphene.Field(ProfileType, username=graphene.String())
    def resolve_profile(root, info, username):
          return Profile.objects.select_related("user").get(
              user__username=username
          )

    # Exercise queries
    exercises = graphene.List(ExerciseType)

    def resolve_exercises(self, info, **kwargs):
        return Exercise.objects.all()

    exercise = graphene.Field(ExerciseType, id=graphene.ID())

    def resolve_exercise(self, info, id):
        return Exercise.objects.get(pk=id)

    # Workout parts queries
    workout_parts = graphene.List(WorkoutPartType)

    def resolve_workout_parts(self, info, **kwargs):
        return WorkoutPart.objects.all()

    # Workout parts queries
    workout_parts_by_workout = graphene.List(WorkoutPartType, id=graphene.ID())

    def resolve_workout_parts_by_workout(self, info, id):
        return Workout.objects.get(pk=id).workout_parts.all()


# Workout parts mutations

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

# Exercise mutations

class MuscleGroup(graphene.Enum):
    LEGS = 'legs'
    HANDS = 'hands'
    BACK = 'back'
    SHOULDERS = 'shoulders'
    CHEST = 'chest'

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


# TrainingApparatus mutations

class Mutation(graphene.ObjectType):
  # Workout
  create_workout = CreateWorkout.Field()
  update_workout = UpdateWorkout.Field()
  delete_workout = DeleteWorkout.Field()
  add_workout_part_to_workout = AddWorkoutPartsToWorkout.Field()
  # Workout parts
  create_workout_part = CreateWorkoutPart.Field()
  update_workout_part = UpdateWorkoutPart.Field()
  delete_workout_parts = DeleteWorkoutParts.Field()
  # Exercise
  create_exercise = CreateExercise.Field()
  update_exercise = UpdateExercise.Field()
  delete_exercise = DeleteExercise.Field()
  # TrainingApparatus
  create_training_apparatus = CreateTrainingApparatus.Field()
  update_training_apparatus = UpdateTrainingApparatus.Field()
  delete_training_apparatus = DeleteTrainingApparatus.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
