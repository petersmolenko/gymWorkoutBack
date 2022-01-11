import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from .models import Workout, WorkoutPart, Exercise, TrainingApparatus, Profile


class WorkoutType(DjangoObjectType):
    class Meta:
        model = Workout

class WorkoutPartType(DjangoObjectType):
    class Meta:
        model = WorkoutPart

class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise

class TrainingApparatusType(DjangoObjectType):
    class Meta:
        model = TrainingApparatus

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class Query(graphene.ObjectType):
  # Profile queries
    profile = graphene.Field(ProfileType, username=graphene.String())
    def resolve_profile(root, info, username):
          return Profile.objects.select_related("user").get(
              user__username=username
          )
  # TrainingApparatus queries
    trainers = graphene.List(TrainingApparatusType)

    def resolve_trainers(self, info, **kwargs):
        return TrainingApparatus.objects.all()


    trainer = graphene.Field(TrainingApparatusType, id=graphene.ID())

    def resolve_trainer(self, info, id):
        return TrainingApparatus.objects.get(pk=id)

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
    
    # Workouts queries
    workouts = graphene.List(WorkoutType)
    completed_workouts = graphene.List(WorkoutType)
    active_workout = graphene.Field(WorkoutType)

    def resolve_workouts(self, info, **kwargs):
        return Workout.objects.all()

    def resolve_active_workout(self, info, **kwargs):
        return Workout.objects.get(in_process=True)

    def resolve_completed_workouts(self, info, **kwargs):
        return Workout.objects.filter(completed=True)

# Workouts mutations

def set_workout_parts(workout, workout_parts_ids):
    workout_parts_set = []

    for w_p in workout_parts_ids:
        w_p_object = WorkoutPart.objects.get(pk=w_p)
        workout_parts_set.append(w_p_object)

    workout.workout_parts.set(workout_parts_set)

class CreateWorkout(graphene.Mutation):
  class Arguments:
    title = graphene.String()
    description = graphene.String()
    workout_parts = graphene.List(graphene.ID)
    completed = graphene.Boolean()
    in_process = graphene.Boolean()
    date = graphene.types.datetime.DateTime()

  workout = graphene.Field(WorkoutType)

  def mutate(
      self,
      info,
      title,
      description,
      workout_parts=None,
      completed=False,
      in_process=False,
      date=None
    ):
    workout = Workout.objects.create(
      title = title,
      description = description,
      completed = completed,
      in_process = in_process,
      date=date
    )

    if workout_parts is not None: set_workout_parts(workout, workout_parts)

    workout.save()

    return CreateWorkout(
      workout=workout
    )

class CommentWorkoutPart(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        comment = graphene.String()

    workoutPart = graphene.Field(WorkoutPartType)


    def mutate(
          self,
          info,
          id,
          comment
        ):
        workoutPart = WorkoutPart.objects.get(pk = id)

        if (workoutPart is None):
            return DeleteWorkout(workoutPart=None)


        workoutPart.comment = comment

        workoutPart.save()

        return CommentWorkoutPart(
          workoutPart=workoutPart
        )


class UpdateWorkout(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    workout_parts = graphene.List(graphene.ID)
    completed = graphene.Boolean()
    in_process = graphene.Boolean()
    date = graphene.types.datetime.DateTime()

  workout = graphene.Field(WorkoutType)

  def mutate(
      self,
      info,
      id,
      title=None,
      description=None,
      workout_parts=None,
      completed=False,
      in_process=False,
      date=None
    ):
    workout = Workout.objects.get(pk=id)
    workout.title = title if title is not None else workout.title
    workout.description = description if description is not None else workout.description
    workout.completed = completed if completed is not None else workout.completed
    workout.in_process = in_process if in_process is not None else workout.in_process
    workout.date = date if date is not None else workout.date

    if workout_parts is not None: set_workout_parts(workout, workout_parts)

    workout.save()

    return UpdateWorkout(
      workout=workout
    )

class DeleteWorkout(graphene.Mutation):
  class Arguments:
    id = graphene.ID()

  workout = graphene.Field(WorkoutType)

  def mutate(
      self,
      info,
      id
    ):
    workout = Workout.objects.get(pk=id)
    if workout is not None:
        workout.delete()

    return DeleteWorkout(
      workout=workout
    )

class AddWorkoutPartToWorkout(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    workoutPartId = graphene.ID()

  workout = graphene.Field(WorkoutType)

  def mutate(self, info, id=None, workoutPartId=None):
    workout = Workout.objects.get(pk=id)
    workoutPart = WorkoutPart.objects.get(pk=workoutPartId)
    workout.workout_parts.add(workoutPart)
    workout.save()
        
    return AddWorkoutPartToWorkout(
      workout=workout
    )


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

class DeleteWorkoutPart(graphene.Mutation):
  class Arguments:
    ids = graphene.List(graphene.ID)

  ok = graphene.Boolean()

  def mutate(
      self,
      info,
      ids=[]
    ):
    try:
      for i in range(len(ids)):
          workoutPart = WorkoutPart.objects.get(pk=ids[i])

          if workoutPart is not None:
              workoutPart.delete()
      return DeleteWorkoutPart(ok=True)
    except:
        return DeleteWorkoutPart(ok=False)
    

    return DeleteWorkoutPart(ok=False)

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

class CreateTrainingApparatus(graphene.Mutation):
  class Arguments:
    title = graphene.String()
    description = graphene.String()
    cover = Upload()

  training_apparatus = graphene.Field(TrainingApparatusType)

  def mutate(
      self,
      info,
      title,
      description,
      cover=None,
    ):
    training_apparatus = TrainingApparatus.objects.create(
      title = title,
      cover = cover,
      description = description
    )

    training_apparatus.save()

    return CreateTrainingApparatus(
      training_apparatus=training_apparatus
    )

class UpdateTrainingApparatus(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    title = graphene.String()
    cover = Upload()

  training_apparatus = graphene.Field(TrainingApparatusType)

  def mutate(
      self,
      info,
      id,
      title=None,
      cover=None,
    ):
    training_apparatus = TrainingApparatus.objects.get(pk=id)
   
    training_apparatus.title = title if title is not None else training_apparatus.title
    training_apparatus.cover = cover if cover is not None else training_apparatus.cover
    
    training_apparatus.save()

    return UpdateTrainingApparatus(
      training_apparatus=training_apparatus
    )

class DeleteTrainingApparatus(graphene.Mutation):
  class Arguments:
    id = graphene.ID()

  ok = graphene.Boolean()

  def mutate(
      self,
      info,
      id
    ):
    try:
      training_apparatus = TrainingApparatus.objects.get(pk=id)

      if training_apparatus is not None:
          training_apparatus.delete()
          return DeleteTrainingApparatus(ok=True)
    except:
        return DeleteTrainingApparatus(ok=False)
    
    return DeleteTrainingApparatus(ok=False)

class Mutation(graphene.ObjectType):
  # Workout
  create_workout = CreateWorkout.Field()
  update_workout = UpdateWorkout.Field()
  delete_workout = DeleteWorkout.Field()
  add_workout_part_to_workout = AddWorkoutPartToWorkout.Field()
  # Workout parts
  create_workout_part = CreateWorkoutPart.Field()
  update_workout_part = UpdateWorkoutPart.Field()
  delete_workout_part = DeleteWorkoutPart.Field()
  # Exercise
  create_exercise = CreateExercise.Field()
  update_exercise = UpdateExercise.Field()
  delete_exercise = DeleteExercise.Field()
  # TrainingApparatus
  create_training_apparatus = CreateTrainingApparatus.Field()
  update_training_apparatus = UpdateTrainingApparatus.Field()
  delete_training_apparatus = DeleteTrainingApparatus.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
