from django.contrib import admin

# Register your models here.
from .models import Dataset, DatasetChart

admin.register(Dataset)
admin.register(DatasetChart)
