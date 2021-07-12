from django.shortcuts import render, redirect
from django.urls import reverse


def video_login(request):
    return render(request, 'videos/video_login.html')


def view_video(request, video_id):
    return redirect(reverse('home'))