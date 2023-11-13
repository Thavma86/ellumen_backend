from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('', include('lotto.urls')),
   path('', include('solarit.urls')),
]