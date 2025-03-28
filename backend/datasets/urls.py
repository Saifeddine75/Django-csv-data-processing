from django.urls import path

from . import views

app_name = "datasets"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.BasicUploadView.as_view(), name="create"),
]
