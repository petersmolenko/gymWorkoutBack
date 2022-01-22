import graphene
from .Type import WorkoutType
from ..WorkoutPart.Type import WorkoutPartType
from gymWorkoutApp.models import Workout, WorkoutPart
from graphene_django.types import DjangoObjectType

# Устанавливет для выбранной тренировки новый этапы
def set_workout_parts(workout, workout_parts_ids):
    workout_parts_set = []

    for w_p in workout_parts_ids:
        w_p_object = WorkoutPart.objects.get(pk=w_p)
        workout_parts_set.append(w_p_object)

    workout.workout_parts.set(workout_parts_set)

    workout.save()

# Создает новую тренировку
class CreateWorkout(graphene.Mutation):
  class Arguments:
    title = graphene.String()
    description = graphene.String()
    workoutParts = graphene.List(graphene.ID)
    date = graphene.String()

  workout = graphene.Field(WorkoutType)

  def mutate(
      self,
      info,
      title,
      description,
      workoutParts
    ):
    workout = Workout.objects.create(
      title = title,
      description = description,
      status = 'b',
    )
    if workoutParts is not None: set_workout_parts(workout, workoutParts)

    workout.save()

    return CreateWorkout(
      workout=workout
    )

# Добавляет комментария для этапа тренировки
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



# Добавляет комментария для этапа тренировки
class StartWorkout(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    workout = graphene.Field(WorkoutType)

    def mutate(
          self,
          info,
          id
        ):
        workout = Workout.objects.get(pk = id)

        workout.status = "a"
        workout.save()

        return StartWorkout(
          workout=workout
        )

# Добавляет комментария для этапа тренировки
class CompleteWorkoutPart(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        wp_id = graphene.ID()

    workout = graphene.Field(WorkoutType)

    def mutate(
          self,
          info,
          id,
          wp_id
        ):
        workout = Workout.objects.get(pk = id)
        workoutPart = WorkoutPart.objects.get(pk = wp_id)
        workoutPart.completed = True
        workoutPart.save()
        workout_status = "c"

        for wp in workout.workout_parts.all():
            if (not wp.completed):
                workout_status = "b"
                break

        workout.status = workout_status
        workout.save()

        return CompleteWorkoutPart(
          workout=workout
        )

# Обновляет тренировку
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

# Удаляет тренировку
class DeleteWorkout(graphene.Mutation):
  class Arguments:
    id = graphene.ID()

  id = graphene.ID()

  def mutate(
      self,
      info,
      id
    ):
    workout = Workout.objects.get(pk=id)
    if workout is not None:
        for w_p in workout.workout_parts.all():
            w_p.delete()
        workout.delete()

    return DeleteWorkout(
      id=id
    )

# Добавляет для тренировки этапы
class AddWorkoutPartsToWorkout(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    workoutPartIds = graphene.List(graphene.ID)

  workout = graphene.Field(WorkoutType)

  def mutate(self, info, id, workoutPartIds):
    workout = Workout.objects.get(pk=id)
    #
    try:
      for i in range(len(workoutPartIds)):
        workoutPart = WorkoutPart.objects.get(pk=workoutPartIds[i])

        if workoutPart is not None:
            workout.workout_parts.add(workoutPart)
      #
      workout.save()
      #
      return AddWorkoutPartsToWorkout(workout=workout)
    except:
      print('error')
      return AddWorkoutPartsToWorkout(workout=None)


class WorkoutMutation(graphene.ObjectType):
    create_workout = CreateWorkout.Field()
    update_workout = UpdateWorkout.Field()
    delete_workout = DeleteWorkout.Field()
    start_workout = StartWorkout.Field()
    complete_workout_part = CompleteWorkoutPart.Field()
    add_workout_part_to_workout = AddWorkoutPartsToWorkout.Field()
