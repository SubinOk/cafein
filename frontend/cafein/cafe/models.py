from django.db import models
from account.models import User

class Cafe(models.Model):

    cafe_id = models.AutoField(primary_key=True)
    name = models.CharField('카페명', max_length=100, null=False, unique = True, error_messages={'unique': "존재하는 카페명입니다"},)
    max_occupancy = models.IntegerField('최대수용인원', null=True)
    address = models.CharField('주소', max_length=100, null=True)
    datail_add = models.CharField('상세주소', max_length=100, null=True)
    cafe_phone = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = 'cafe'
    

class Cafe_image(models.Model):

    image_id = models.AutoField(primary_key=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField('카페IMAGE', upload_to='cafe/', blank=True, null=True)
    
    class Meta:
        db_table = 'cafe_image'
    
class Cafe_menu(models.Model):

    menu_id = models.AutoField(primary_key = True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE , blank=True, null =True)
    name = models.CharField('메뉴명', max_length=100, null=True)
    price = models.CharField('가격', max_length=100, null=True)
    image = models.ImageField('메뉴IMAGE', upload_to='cafeMenu/', blank=True, null=True)
    #혼잡도 추가 
    class Meta:
        db_table = 'cafe_menu'

class Cafe_review(models.Model):
    review_id = models.AutoField(primary_key = True)

    