from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.http import JsonResponse

from customer.forms import customerPostForm, createViewForm
from cafe.models import Cafe, Cafe_review, Cafe_comment, Cafe_image, Cafe_congestion, Cafe_menu
from account.models import User
from django.db.models import Q

def customerHome(request):
    if request.session.get('user'):
        return render(request, 'customerHome.html', {'title': '고객홈'})
    else:
        return redirect('/')
    
def getCafeData(request):
    cafes = Cafe.objects.all()
    cafe_image = []
    for cafe in cafes:
        cafe_image.append(Cafe_image.objects.filter(cafe=cafe)[0])
    
    paginator = Paginator(cafe_image, 6)

    page_number = request.GET.get('page')
    cafe_images_page = paginator.get_page(page_number)
    
    if int(page_number) == int(paginator.num_pages):
        last_page = True
    else:
        last_page = False
    cafe_images = []
    customer = User.objects.filter(email=request.session.get('user'))[0]
    for cafe_image in cafe_images_page.object_list:
        cafe_congestion_cnt = Cafe_congestion.objects.get(cafe=cafe_image.cafe).congestion
        # 40 미만
        if cafe_congestion_cnt < 40:
            cafe_congestion = "good"
        # 70 미만
        elif cafe_congestion_cnt < 70:
            cafe_congestion = "soso"
        # 이외
        else:
            cafe_congestion = "bad"

        if customer in cafe_image.cafe.like_users.all():
            like = True
        else:
            like = False

        cafe_images.append({
            'cafe': cafe_image.cafe.name,
            'cafe_id': cafe_image.cafe.cafe_id,
            'image': cafe_image.image.url,
            'cafe_congestion': cafe_congestion,
            'like': like
                            })

    return JsonResponse({'cafe_images': cafe_images, 'last_page': last_page})

def signup(request):
    if not(request.session.get('user')):
        if request.method == 'POST':
            form = customerPostForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.check_email():
                    return render_with_error(request, 'signup2.html', form, ['email'], '고객 회원가입')
                if not (form.check_password1() and form.check_password()):
                    return render_with_error(request, 'signup2.html', form, ['password'], '고객 회원가입')
                if not form.check_phone():
                    return render_with_error(request, 'signup2.html', form, ['phone'], '고객 회원가입')
                
                form.save()
                # Save 성공시에는 Redirect
                request.session['user'] = request.POST.get('email')
                request.session['is_owner'] = False
                return redirect('/customer/home')
        else:
            form = customerPostForm()
            return render(request, 'signup2.html', {'form': form, 'title': '고객 회원가입'})
    return redirect('/')

def cafeHome(request, cafeId):
    if request.method == "POST":
        pass
    else:
        cafe = Cafe.objects.get(cafe_id=cafeId)
        customer = User.objects.filter(email=request.session.get('user'))[0]
        cafe_reviews = Cafe_review.objects.filter(cafe=cafe).order_by('-date')[:3]
        cafe_menu = Cafe_menu.objects.filter(cafe=cafe)
    return render(request, 'cafeHome.html', {'cafe': cafe, 'customer':customer, 'reviews':cafe_reviews, 'cafe_menu': cafe_menu, 'title': cafe.name+' 홈'})

def cafeReview(request):
    
    cafe_reviews = Cafe_review.objects.all().order_by('-date')

    paginator = Paginator(cafe_reviews, 2)

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    return render(request, 'cafeReview.html', {'reviews': page_reviews, 'title': '리뷰 게시판'})

def cafeReviewDetail(request, cafeId, reviewid):
    cafe = Cafe.objects.get(cafe_id=cafeId)
    cafe_review = Cafe_review.objects.get(cafe=cafe, review_id=reviewid)
    cafe_comment = Cafe_comment.objects.get(review=reviewid)
    
    contents = {
        'cafe_review' : cafe_review,
        'cafe_comment': cafe_comment,
        'cafeId': cafeId,
    }
    return render(request, 'cafeReviewDetail.html', {'contents': contents, 'title': '리뷰 게시판'})

def createReview(request, cafeId):
    if request.method == 'POST':
        form = createViewForm(request.POST)
        if form.is_valid():
            cafeReview = form.save()
            cafeReview.image = request.FILES.get('image')
            cafeReview.cafe = Cafe.objects.get(cafe_id=cafeId)
            cafeReview.score = request.POST.get('bean_score')
            cafeReview.comment = Cafe_comment.objects.create(
                review=cafeReview,
                writer=User.objects.get(user_id=cafeReview.cafe.user)
            )
            cafeReview.writer = User.objects.get(user_id=request.session.get('user'))
            cafeReview.save()
            return redirect('/customer/'+str(cafeReview.cafe.cafe_id)+'/review/'+str(cafeReview.review_id))
    else:
        form = createViewForm()
        return render(request, 'cafeCreateReview.html', {'form': form, 'title': '리뷰 작성'})

def render_with_error(request, html, form, error_type, title=''):
    error_flg = {}
    for error in error_type:
        error_flg[error] = True
    return render(request, html, {'form': form, 'error_flg': error_flg, 'title': title})

def cafeLike(request, cafeId):
    cafe = get_object_or_404(Cafe, cafe_id=cafeId)
    customer = User.objects.filter(email=request.session.get('user'))[0]
    if customer in cafe.like_users.all():
        cafe.like_users.remove(customer)
    else:
        cafe.like_users.add(customer)
    return redirect('/customer/'+str(cafeId)+'/home')


def index(request):
    customer = User.objects.filter(email=request.session.get('user'))[0]
    cafes = customer.like_users.all()
    cafe_images = []

    for cafe in cafes:
        cafe_image = Cafe_image.objects.filter(cafe=cafe)[0]
        cafe_congestion = Cafe_congestion.objects.get(cafe=cafe_image.cafe).congestion

        cafe_images.append({
            'cafe_image': cafe_image,
            'cafe_congestion': cafe_congestion,
                            })
    return render(request, 'cafeLike.html', {'cafe_image': cafe_images, 'title': '즐겨찾는 카페'})

def cafeIdReview(request, cafeId):
    cafe_reviews = Cafe_review.objects.filter(cafe=Cafe.objects.get(cafe_id=cafeId)).order_by('-date')

    paginator = Paginator(cafe_reviews, 2)

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    return render(request, 'cafeReview.html', {'reviews': page_reviews, 'title': '리뷰 게시판'})