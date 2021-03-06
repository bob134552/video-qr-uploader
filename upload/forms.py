from django import forms
from .models import Videos


class UploadForm(forms.ModelForm):

    class Meta:
        model = Videos
        fields = (
            'email',
            'order_number',
            'keyword',
        )

    keyword = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyword'].widget.attrs['aria-describedby'] = 'keywordHelpBlock'


class VideoForm(forms.ModelForm):

    class Meta:
        model = Videos
        fields = (
            'video',
        )

    video = forms.FileField(required=True, widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video'].label = False
