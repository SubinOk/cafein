from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class User(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'M','남성'
        FEMALE = 'F','여성'

    user_id = models.EmailField(max_length = 100,primary_key=True)
    password = models.CharField(max_length=300) # 암호화 해야하니까 넉넉히300
    name = models.CharField(max_length=20)
    
    # phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    # phone = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True,default='')
    phone  = models.CharField(max_length=25, unique = True, default='')
    gender = models.CharField(choices=GenderChoices.choices, max_length=1, blank=True,default='')
    age = models.CharField(max_length=10, default='')

    class Meta:
        db_table = 'user'
