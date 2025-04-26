from django.urls import path
from .views import UploadView, ResultsView

urlpatterns = [
    path('', UploadView.as_view(), name='upload'),
    path('results/', ResultsView.as_view(), name='results'),
]