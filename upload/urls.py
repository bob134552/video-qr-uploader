from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_login, name='upload_login'),
]
