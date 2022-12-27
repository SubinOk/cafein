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

    class Meta:
        db_table = 'cafe_menu'

class Cafe_review(models.Model):
    review_id = models.AutoField('리뷰id', primary_key = True)
    #review_id = models.IntegerField('리뷰id',primary_key = True)
    title = models.CharField('리뷰제목', max_length=100, null=True)
    score = models.IntegerField('별점', validators=[MinValueValidator(1), MaxValueValidator(5)], default=False)
    content = models.TextField('리뷰내용', blank=False)
    deleted = models.BooleanField('삭제여부', default=False) #삭제했을 때 '삭제한 리뷰입니다'로 표시하기
    image = models.ImageField('리뷰IMAGE', upload_to='cafe/review/', blank=True, null=True)
    date = models.DateTimeField('작성일', auto_now_add = True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE , blank=True, null =True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
   
      
    class Meta:
        db_table = 'cafe_review'

class Cafe_comment(models.Model):
    comment_id = models.AutoField(primary_key = True)
    content = models.TextField('리뷰내용', blank=False)
    deleted = models.BooleanField('삭제여부', default=False)  #삭제했을 때 '삭제한 댓글입니다'로 표시하기
    date = models.DateTimeField('작성일', auto_now_add = True)
    review = models.ForeignKey(Cafe_review, on_delete=models.CASCADE , blank=True, null =True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'cafe_comment'

class Cafe_sentiment(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE , blank=True, null =True)
    sentiment_id = models.AutoField(primary_key = True)
    total = models.DecimalField('전체긍정비율', max_digits = 5, decimal_places=3)

    price_rank = models.IntegerField()
    price_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)

    drink_rank = models.IntegerField()
    drink_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)

    dessert_rank = models.IntegerField()
    dessert_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)

    service_rank = models.IntegerField()
    service_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)

    customers_rank = models.IntegerField()
    customers_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)

    interior_rank = models.IntegerField()
    interior_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)

    view_rank = models.IntegerField()
    view_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)

    parking_rank = models.IntegerField()
    parking_sentiment = models.DecimalField(max_digits = 5, decimal_places=3)


    class Meta:
        db_table = 'cafe_sentiment'

class Cafe_keyword(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE , blank=True, null =True)
    keyword_id = models.AutoField(primary_key = True)

    price_word = models.CharField(max_length=100, null=True)
    price_count = models.IntegerField(default=0)

    drink_word = models.CharField(max_length=100, null=True)
    drink_count = models.IntegerField(default=0)

    dessert_word = models.CharField(max_length=100, null=True)
    dessert_count = models.IntegerField(default=0)

    service_word = models.CharField(max_length=100, null=True)
    service_count = models.IntegerField(default=0)

    customers_word = models.CharField(max_length=100, null=True)
    customers_count = models.IntegerField(null =True)

    interior_word = models.CharField(max_length=100, null=True)
    interior_count = models.IntegerField(null =True)

    view_word = models.CharField(max_length=100, null=True)
    view_count = models.IntegerField(null =True)

    parking_word = models.CharField(max_length=100, null=True)
    parking_count = models.IntegerField(null =True)
    
    class Meta:
        db_table = 'cafe_keyword'

class Cafe_favorites(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)

    favorites_id = models.AutoField(primary_key = True)
    cafe = models.ManyToManyField(
        "cafe.Cafe",
        related_name="cafe_list",
        blank=True
    )

    class Meta:
        db_table = 'cafe_favorites'

    

class Cafe_congestion(models.Model):
    favorites_id = models.AutoField(primary_key = True)
    congestion = models.IntegerField(null =True)

    class Meta:
        db_table = 'cafe_congestion'




    

    