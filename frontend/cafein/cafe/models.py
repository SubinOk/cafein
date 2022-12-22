from django.db import models
from account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



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
    image = models.ImageField('메뉴IMAGE', upload_to='cafe/menu/', blank=True, null=True)
    #혼잡도 추가 

    class Meta:
        db_table = 'cafe_menu'

class Cafe_review(models.Model):
    review_id = models.AutoField('리뷰id', primary_key = True)
    #review_id = models.IntegerField('리뷰id',primary_key = True)
    title = models.CharField('리뷰제목', max_length=100, null=True)
    score = models.IntegerField('별점', validators=[MinValueValidator(1), MaxValueValidator(5)], default=False)
    content = models.TextField('리뷰내용', default=False)
    deleted = models.BooleanField('삭제여부', default=False) #삭제했을 때 '삭제한 리뷰입니다'로 표시하기
    image = models.ImageField('리뷰IMAGE', upload_to='cafe/review/', blank=True, null=True)
    date = models.DateTimeField('작성일', auto_now_add = True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE , blank=True, null =True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    review_id2 = models.IntegerField('카페별id')
      
    class Meta:
        db_table = 'cafe_review'

class Cafe_comment(models.Model):
    comment_id = models.AutoField(primary_key = True)
    content = models.TextField('리뷰내용',default=False)
    deleted = models.BooleanField('삭제여부', default=False)  #삭제했을 때 '삭제한 댓글입니다'로 표시하기
    date = models.DateTimeField('작성일', auto_now_add = True)
    review = models.ForeignKey(Cafe_review, on_delete=models.CASCADE , blank=True, null =True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'cafe_comment'

    

    

    