import graphene
#
from .models.Trainer.Query import TrainerQuery
from .models.Trainer.Mutation import TrainerMutation
#
from .models.Workout.Query import WorkoutQuery
from .models.Workout.Mutation import WorkoutMutation
#
from .models.WorkoutPart.Query import WorkoutPartsQuery
from .models.WorkoutPart.Mutation import WorkoutPartsMutation
#
from .models.Exercise.Query import ExerciseQuery
from .models.Exercise.Mutation import ExerciseMutation

class Query(
    ExerciseQuery,
    TrainerQuery,
    WorkoutQuery,
    WorkoutPartsQuery,
    graphene.ObjectType
):
    pass

class Mutation(
    TrainerMutation,
    ExerciseMutation,
    WorkoutPartsMutation,
    WorkoutMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
