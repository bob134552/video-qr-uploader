from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from .forms import UploadForm, VideoForm
from .models import Videos
import shopify
import moviepy.editor

def upload_login(request):

    if request.method == 'POST':
        shopify.ShopifyResource.set_site(settings.SHOP_URL)
        orders = shopify.Order.find()

        data = {
            'order_number': request.POST['order_number'],
            'email': request.POST['email'],
            'keyword': request.POST['keyword']
        }
        
        for i, order in enumerate(orders):
            if order.order_number == int(data['order_number']) and order.email == data['email']:
                video = Videos.objects.filter(
                    order_number=data['order_number'], email=data['email'])
                if video.exists():
                    if data['keyword'] == video[0].keyword:
                        request.session['pp_upload_login'] = True
                        return redirect(reverse('upload_video', args=[video[0].id]))
                    else:
                        messages.warning(
                            request, 'Incorrect details entered, please try again.')
                        return redirect('upload_login')
                else:
                    form = UploadForm(data)
                    if form.is_valid():
                        new_video = form.save()
                        request.session['pp_upload_login'] = True
                        messages.success(
                            request, 'Please upload or record your video.')
                        return redirect(reverse('upload_video', args=[new_video.id]))
                    else:
                        messages.error(request, 'Please ensure form is valid.')
                        return redirect('upload_login')
            else:
                if i == len(orders) - 1:
                    messages.error(request, 'Order Number/Email doesn\'t match with Shopify Order details.')
                    return redirect('upload_login')
    else:
        email = request.GET.get('email') if request.GET.get(
            'email') is not None else ""
        order_number = request.GET.get('order_number') if request.GET.get(
            'order_number') is not None else ""

        form = UploadForm(initial={
            'email': email,
            'order_number': order_number,
        })

        context = {
            'form': form
        }

        return render(request, 'upload/upload_login.html', context)


def upload_video(request, video_id):
    if 'pp_upload_login' in request.session:
        video = get_object_or_404(Videos, pk=video_id)
        if request.method == 'POST':
            v = moviepy.editor.VideoFileClip(request.FILES['video'].temporary_file_path())
            duration = v.duration
            if duration <= 30 and duration > 0:
                form = VideoForm(request.POST, request.FILES, instance=video)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Video Uploaded!')
                else:
                    messages.error(request, 'Upload Failed.')
                return redirect(reverse('upload_video', args=[video_id]))
            else:
                messages.error(request, 'Please ensure video duration is less than 30s.')
                return redirect(reverse('upload_video', args=[video_id]))
        else:
            form = VideoForm()
            context = {
                'video': video,
                'form': form,
            }
            return render(request, 'upload/upload_video.html', context)
    else:
        return redirect(reverse('home'))
