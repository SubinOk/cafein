from django.db import models


class Cafe(models.Model):

    cafe_id = models.AutoField(primary_key=True)
    name = models.CharField('카페명', max_length=100, null=False, unique = True, error_messages={'unique': "존재하는 카페명입니다"},)
    max_occupancy = models.IntegerField('최대수용인원', null=True)
    address = models.CharField('주소', max_length=100, null=True)
    datail_add = models.CharField('상세주소', max_length=100, null=True)
    cafe_phone = models.CharField(max_length=50, null=True)
    
    class Meta:
        db_table = 'cafe'


class Cafe_image(models.Model):

    image_id = models.AutoField(primary_key=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField('카페IMAGE', upload_to='cafe/', blank=True, null=True)
    
    class Meta:
        db_table = 'cafe_image'
