from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from upload.models import Videos
from django.conf import settings

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def video_login(request):
    '''
    Renders video login page.
    On post takes order_number and keyword to log into the video page.
    pp_video_login set to prevent user from bypassing login.
    '''
    if request.method == 'POST':
        data = {
            'order_number': request.POST['order_number'],
            'keyword': request.POST['keyword'],
        }
        try:
            video = Videos.objects.get(
                order_number=data['order_number'], keyword=data['keyword'])
            request.session['pp_video_login'] = video.id
            return redirect(reverse('view_video', args=[video.id]))
        except Videos.DoesNotExist:
            messages.error(request, 'Incorrect Order Number/Keyword. Please try again.')
            return redirect('video_login')
    else:
        order_number = request.GET.get('order_number') if request.GET.get(
            'order_number') is not None else ""
        keyword = request.GET.get('keyword') if request.GET.get(
            'keyword') is not None else ""

        context = {
            'order_number': order_number,
            'keyword': keyword,
        }

        return render(request, 'videos/video_login.html', context)


def view_video(request, video_id):
    '''
    Renders video page.
    On post, takes name and message to send a reply email to the user that uploaded the
    video.
    '''
    if 'pp_video_login' in request.session:
        if request.session['pp_video_login'] == video_id:
            video = Videos.objects.get(pk=video_id)
            if request.method == 'POST':
                subject = f'QRit: #{ video.order_number }'
                name = request.POST['name']
                body = request.POST['message']
                html_message = render_to_string('videos/email_templates/email_template.html', {
                    'name' : name,
                    'body': body,
                    'video': video,
                    })
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                to = video.email

                video.reply = True
                video.save()
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                messages.success(request, f'Message Sent to {video.email}!')
                return redirect(reverse('view_video', args=[video_id]))
            else:
                context = {
                    'video': video,
                }

                return render(request, 'videos/video.html', context)
        else:
            messages.warning(request, 'Please enter details to view video.')
            return redirect(reverse('video_login'))
    else:
        messages.warning(request, 'Please enter details to view video.')
        return redirect(reverse('video_login'))

