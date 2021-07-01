from django import forms
from .models import Videos


class VideoForm(forms.ModelForm):

    class Meta:
        model = Videos
        fields = (
            'email',
            'order_number',
            'keyword',
        )
    
    keyword = forms.CharField(widget=forms.PasswordInput)
