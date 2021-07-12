from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_login, name='video_login'),
    path('<int:video_id>', views.view_video, name='view_video'),
]
