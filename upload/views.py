from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from .forms import UploadForm, VideoForm
from .models import Videos
import shopify
import moviepy.editor


def upload_login(request):
    ''' Renders the upload login page.
        If directed to this page via qr code then the email and order_number fields are prefilled.
        On post shopify is queried for orders and checked to see if the order number exists in
        the shopify store.
        Post request requires the users email, order_number and a keyword.
    '''
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
                        request.session['pp_upload_login'] = video[0].id
                        return redirect(reverse('upload_video', args=[video[0].id]))
                    else:
                        messages.warning(
                            request, 'Incorrect details entered, please try again.')
                        return redirect('upload_login')
                else:
                    form = UploadForm(data)
                    if form.is_valid():
                        new_video = form.save()
                        request.session['pp_upload_login'] = new_video.id
                        messages.success(
                            request, 'Please upload or record your video.')
                        return redirect(reverse('upload_video', args=[new_video.id]))
                    else:
                        messages.error(request, 'Please ensure form is valid.')
                        return redirect('upload_login')
            else:
                if i == len(orders) - 1:
                    messages.error(
                        request, 'Order Number/Email doesn\'t match with Shopify Order details.')
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
    '''
    Renders video upload page for specified video_id.
    Takes a video file to add to the specific video model.
    Checks length of video to ensure 30s maximum.
    '''
    if 'pp_upload_login' in request.session:
        if request.session['pp_upload_login'] == video_id:
            video = get_object_or_404(Videos, pk=video_id)
            if request.method == 'POST':
                if request.FILES['video'].content_type == "video/webm":
                    form = VideoForm(request.POST, request.FILES, instance=video)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Video Uploaded!')
                        return render(request, 'upload/upload_success.html')
                    else:
                        messages.error(request, 'Upload Failed.')
                    return redirect(reverse('upload_video', args=[video_id]))
                else:
                    v = moviepy.editor.VideoFileClip(request.FILES['video'].file.name)
                    duration = v.duration
                    if duration <= 60 and duration > 0:
                        form = VideoForm(request.POST, request.FILES, instance=video)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Video Uploaded!')
                            return render(request, 'upload/upload_success.html')
                        else:
                            messages.error(request, 'Upload Failed.')
                        return redirect(reverse('upload_video', args=[video_id]))
                    else:
                        messages.error(
                            request, 'Please ensure video duration is less than 60s.')
                    return redirect(reverse('upload_video', args=[video_id]))
            else:
                form = VideoForm()
                context = {
                    'video': video,
                    'form': form,
                }
                return render(request, 'upload/upload_video.html', context)
        else:
            messages.warning(request, 'Please fill in details.')
            return redirect(reverse('upload_login'))
    else:
        messages.warning(request, 'Please fill in details.')
        return redirect(reverse('upload_login'))
