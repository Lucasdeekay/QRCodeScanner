from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone_no = models.CharField(max_length=20)
    qr_image = models.ImageField(upload_to='qrcodes', blank=True)

    def __str__(self):
        return self.full_name
