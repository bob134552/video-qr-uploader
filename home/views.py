from django.shortcuts import render


def home(request):
    '''Renders home page'''
    if 'pp_upload_login' in request.session:
        del request.session['pp_upload_login']
    return render(request, 'home/index.html')
