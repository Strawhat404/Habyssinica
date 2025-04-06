# recommender/models.py
from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    cost = models.FloatField(default=0.0)
    interests = models.JSONField()  # Stores list of interests (e.g., ["history", "culture"])
    season = models.CharField(max_length=50, default="Year-round")
    location = models.CharField(max_length=100, default="Ethiopia")

    def __str__(self):
        return self.name