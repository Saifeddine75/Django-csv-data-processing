from django.db import models
from django.utils import timezone
# TODO: use ArrayField
# from django.contrib.postgres.fields import ArrayField

class Dataset(models.Model):
    title = models.CharField(max_length=255, default=timezone.now)  # To store the title of the chart
    timestamp = models.JSONField(models.FloatField(), default=list)  # To store the timestamp values
    x = models.JSONField(models.FloatField(), default=list)
    y = models.JSONField(models.FloatField(), default=list)
    z = models.JSONField(models.FloatField(), default=list)
    norm = models.JSONField(models.FloatField(), default=list)
    stats = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Data from {self.timestamp} (x: {self.x}, y: {self.y}, z: {self.z})"
    

class DatasetChart(models.Model):
    title = models.CharField(max_length=255, default=timezone.now)  # To store the title of the chart
    plot_data = models.JSONField(default=dict)  # To store the chart data as a JSON object
    stats = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title  # Display the title in the admin panel or elsewhere