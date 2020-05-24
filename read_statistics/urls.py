from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/statistics
    path('',views.statistics,name='statistics'),
]