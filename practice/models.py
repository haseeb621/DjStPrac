from django.db import models
from django.contrib.auth.models import User
from djstripe.models import Customer
# Create your models here.
class Profile(models.Model):
 user=models.OneToOneField(User,on_delete=models.CASCADE)
 customer=models.OneToOneField(Customer,on_delete=models.CASCADE)
 djstripe_id = models.CharField(max_length=50, unique=True,default='')
 