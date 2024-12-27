from django.urls import path
from .views import UploadFileViewSet

urlpatterns = [
    path('upload/', UploadFileViewSet.as_view())
]