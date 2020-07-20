from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 50, blank = False)
    email = models.EmailField(unique = True, blank = False)
    password = models.CharField(max_length = 50, blank = False)
    otp = models.IntegerField(blank = True, default = 0)
    # mobile = models.IntegerField(max_length = 10, blank = True)