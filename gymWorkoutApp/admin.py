from django.contrib import admin

from gymWorkoutApp.models import Profile, TrainingApparatus, Exercise, WorkoutPart, Workout

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile

@admin.register(TrainingApparatus)
class TrainingApparatusAdmin(admin.ModelAdmin):
    model = TrainingApparatus

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    model = Exercise

@admin.register(WorkoutPart)
class WorkoutPartAdmin(admin.ModelAdmin):
    model = WorkoutPart

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    model = Workout
