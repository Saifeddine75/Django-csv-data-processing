from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Dataset(models.Model):
    title = models.CharField(max_length=255, default=timezone.now)  # To store the title of the chart
    timestamp = ArrayField(models.FloatField(), default=list)  # To store the timestamp values
    x = ArrayField(models.FloatField(), default=list)
    y = ArrayField(models.FloatField(), default=list)
    z = ArrayField(models.FloatField(), default=list)
    norm = ArrayField(models.FloatField(), default=list)
    stats = models.JSONField(models.FloatField(), default=dict)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Data from {len(self.timestamp)} (x: {len(self.x)}, y: {len(self.y)}, z: {len(self.z)})"
    

class DatasetChart(models.Model):
    title = models.CharField(max_length=255, default=timezone.now)  # To store the title of the chart
    plot_data = ArrayField(models.FloatField(), default=dict)  # To store the chart data as a JSON object
    stats = ArrayField(models.FloatField(), default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title  # Display the title in the admin panel or elsewhere