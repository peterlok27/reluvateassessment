from django.db import models
from django.contrib.auth.models import  User

# Create your models here.
class Pokemon(models.Model):
    # ID field not necessary to be included, as the primary key is initialized by default. 
    name = models.CharField(max_length=30) 
    hp = models.IntegerField() # Remember that certain values should not be negative. Data Validation necessary
    attack =models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(max_length=30)
    level = models.IntegerField(default=0) 
    owner = models.ForeignKey(User,null=True,verbose_name = 'User', on_delete=models.SET_NULL, default=None) # SET_NULL means that when the user is deleted, the pokemon will be sent into wild

