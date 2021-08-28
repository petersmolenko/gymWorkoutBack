from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.user.get_username()


class TrainingApparatus(models.Model):
    title = models.CharField(max_length=50, unique=True)
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

class Exercise(models.Model):
    MUSCLE_GROUPS = [
        ('legs', 'Ноги'),
        ('hands', 'Руки'),
        ('back', 'Спина'),
        ('shoulders', 'Плечи'),
        ('chest', 'Грудь'),
    ]
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    training_apparatus = models.ForeignKey(TrainingApparatus, on_delete=models.PROTECT)
    muscle_group = models.CharField(
        max_length=20,
        choices=MUSCLE_GROUPS,
        default='hands',
    )

    def __str__(self):
        return self.title

class WorkoutPart(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    weight = models.FloatField(max_length=1000)
    repetitions_number = models.IntegerField()
    sort_order = models.IntegerField()
    completed = models.BooleanField()

    def __str__(self):
        return self.title

class Workout(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    workout_parts = models.ManyToManyField(WorkoutPart, blank=True)
    completed = models.BooleanField()
    in_process = models.BooleanField()
    date = models.DateField()


    def __str__(self):
        return self.title