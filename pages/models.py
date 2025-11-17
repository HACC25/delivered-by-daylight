from django.core.validators import MaxValueValidator
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    major = models.CharField(max_length=100)  # e.g. "Accounting", "Psychology"
    coursenumber = models.PositiveIntegerField(
        default=100,
        validators=[MaxValueValidator(499)]
    )
    def __str__(self):
        return self.title

