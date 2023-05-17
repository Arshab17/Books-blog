from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserOTP(models.Model):
    otp = models.CharField(max_length=5)
    user = models.OneToOneField(User,on_delete=models.CASCADE)