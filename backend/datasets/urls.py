from django.urls import path
from .views import DatasetUploadView

urlpatterns = [
    path('', DatasetUploadView.as_view(), name='upload_dataset'),  # Base datasets URL
    path("delete-dataset/<int:id>/", DatasetUploadView.delete_dataset, name="delete_dataset"),
]