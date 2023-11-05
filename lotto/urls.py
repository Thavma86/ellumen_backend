from . import views
from django.urls import path

urlpatterns = [
    path('api/lotto/', views.find_counter, name='lotto')
]