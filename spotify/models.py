from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Settings(models.Model):
    show_albums = models.BooleanField()
    explicit = models.BooleanField()
    clean = models.BooleanField()
    minPop = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    maxPop = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])