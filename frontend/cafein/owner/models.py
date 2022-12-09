from django.db import models
from cafe.models import Cafe

class Owner(models.Model):
    
    owner_id = models.EmailField(max_length = 100,primary_key=True ,default='')
    password = models.CharField(max_length=300, default='')
    phone = models.CharField(max_length=25, unique = True , default='')
    cafe = models.ForeignKey(Cafe,on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = 'owner'


        

