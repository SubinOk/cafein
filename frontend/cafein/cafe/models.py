from django.db import models
from account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):
    #파일에 같은 이름이 존재하는 경우에 ovewrite하기
    def get_available_name(self, name,max_length = None):
        if self.exists(name):
            print(name)
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
        

class Cafe(models.Model):

    cafe_id = models.AutoField(primary_key=True)
    name = models.CharField('카페명', max_length=100, null=False, unique = True, error_messages={'unique': "존재하는 카페명입니다"},)
    max_occupancy = models.IntegerField('최대수용인원', null=True)
    address = models.CharField('주소', max_length=100, null=True)
    datail_add = models.CharField('상세주소', max_length=100, null=True)
    cafe_phone = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    like_users = models.ManyToManyField(User, related_name="like_users",blank=True )
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
    price = models.IntegerField('가격', null=True)
    image = models.ImageField('메뉴IMAGE', max_length=255, upload_to='cafe/menu/', blank=True, null=True)

    class Meta:
        db_table = 'cafe_menu'

class Cafe_review(models.Model):
    review_id = models.AutoField('리뷰id', primary_key = True)
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
    total_count = models.IntegerField(null=True)

    class Meta:
        db_table = 'cafe_sentiment'

class Cafe_rank(models.Model):
    rank_id = models.AutoField(primary_key = True)
    category = models.CharField(max_length=100, null=True)
    rank = models.IntegerField('순위', null=True)
    ratio = models.DecimalField('카테고리별 긍정비율',max_digits = 5, decimal_places=3)
    sentiment = models.ForeignKey(Cafe_sentiment, on_delete=models.CASCADE , blank=True, null =True)
    cnt = models.IntegerField(null=True)
    positive_cnt = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'cafe_rank'

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

class Cafe_congestion(models.Model):
    congestion_id = models.AutoField(primary_key = True)
    congestion = models.IntegerField(null =True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE , blank=True, null =True)
    
    class Meta:
        db_table = 'cafe_congestion'

class Cafe_wordcloud(models.Model):
    word_id = models.AutoField(primary_key= True)
    price = models.ImageField('price', upload_to="wordcloud/", blank=True, null=True,storage=OverwriteStorage())
    drink = models.ImageField('drink IMAGE', upload_to="wordcloud/",  blank=True, null=True,storage=OverwriteStorage())
    dessert = models.ImageField('dessert IMAGE', upload_to="wordcloud/",  blank=True, null=True,storage=OverwriteStorage())
    service = models.ImageField('service IMAGE', upload_to="wordcloud/",  blank=True, null=True,storage=OverwriteStorage())
    customers = models.ImageField('customers IMAGE', upload_to="wordcloud/",  blank=True, null=True,storage=OverwriteStorage())
    interior = models.ImageField('interior IMAGE', upload_to="wordcloud/",  blank=True, null=True,storage=OverwriteStorage())
    view = models.ImageField('view IMAGE', upload_to="wordcloud/",  blank=True, null=True,storage=OverwriteStorage())
    parking = models.ImageField('parking IMAGE', upload_to="wordcloud/",  blank=True, null=True,storage=OverwriteStorage())
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE , blank=True, null =True)

    class Meta:
        db_table = 'cafe_wordcloud'

