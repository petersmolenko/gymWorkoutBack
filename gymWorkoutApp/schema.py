import graphene
from graphene_django import DjangoObjectType
from .models import Workout, WorkoutPart, Exercise


class WorkoutType(DjangoObjectType):
    class Meta:
        model = Workout

class WorkoutPartType(DjangoObjectType):
    class Meta:
        model = WorkoutPart

class Query(graphene.ObjectType):
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
    id = graphene.ID()

  ok = graphene.Boolean()

  def mutate(
      self,
      info,
      id
    ):
    try:
      workoutPart = WorkoutPart.objects.get(pk=id)

      if workoutPart is not None:
          workoutPart.delete()
          return DeleteWorkoutPart(ok=True)
    except:
        return DeleteWorkoutPart(ok=False)
    

    return DeleteWorkoutPart(ok=False)

class Mutation(graphene.ObjectType):
  create_workout = CreateWorkout.Field()
  update_workout = UpdateWorkout.Field()
  delete_workout = DeleteWorkout.Field()
  add_workout_part_to_workout = AddWorkoutPartToWorkout.Field()

  create_workout_part = CreateWorkoutPart.Field()
  update_workout_part = UpdateWorkoutPart.Field()
  delete_workout_part = DeleteWorkoutPart.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)