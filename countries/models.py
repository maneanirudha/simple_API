from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Countries(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50,blank=False,default='')
    capital = models.CharField(max_length=50,blank=False,default='')


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)