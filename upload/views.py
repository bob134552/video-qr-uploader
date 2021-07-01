from django.shortcuts import render
from django.conf import settings
from .forms import VideoForm
import shopify

def upload_login(request):

    if request.method == 'POST':
        shopify.ShopifyResource.set_site(settings.SHOP_URL)
        orders = shopify.Order.find()
    
    else:

        form = VideoForm()

        context = {
            'form': form
        }

    return render(request, 'upload/upload_login.html', context)
