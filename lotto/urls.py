from . import views
from django.urls import path

urlpatterns = [
    path('api/lotto/', views.get_reponse_from_lotto_machine, name='lotto')
]