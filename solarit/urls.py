from . import views
from django.urls import path

urlpatterns = [
    path('api/solaritchatbot/', views.get_chatbot_response, name='solaritchatbot'),
    path('api/getfiles/', views.get_all_serialized_documents, name='getfiles'),
    path('api/postfiles/', views.save_docs, name='savedocs'),
    path('api/delete/<str:documentid>/', views.delete_doc, name='delete'),
    path('api/systemtemplate/', views.post_chatbot_system_role, name='system_template'),
    path('api/getsystemtemplate/', views.get_chatbot_system_role, name='get_system_template'),
]