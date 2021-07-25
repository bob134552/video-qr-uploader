import os

from django.db import models
from django.dispatch import receiver
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import qrcode


class Videos(models.Model):
    class Meta:
        ordering = ('-order_number',)
        verbose_name_plural = 'Videos'

    order_number = models.CharField(max_length=256, null=False, blank=False)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    keyword = models.CharField(max_length=20, null=False, blank=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return str(self.order_number)

    def save(self, *args, **kwargs):
        qr_code_img = qrcode.make(f'www.QRit.com/video/?order_number={self.order_number}&keyword={self.keyword}')
        canvas = Image.new('RGB', (400, 400), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_code_img)
        fname = f'qr_code-{self.order_number}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
