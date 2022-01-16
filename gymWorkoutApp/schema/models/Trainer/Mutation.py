import graphene
from .Type import TrainingApparatusType
from gymWorkoutApp.models import TrainingApparatus
from graphene_file_upload.scalars import Upload

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

