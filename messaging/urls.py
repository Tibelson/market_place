from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('start/<int:item_id>/', views.start_chat, name='start_chat'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
]
