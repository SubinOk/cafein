from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from customer.forms import customerPostForm, createViewForm
from cafe.models import Cafe, Cafe_review, Cafe_comment, Cafe_image
from account.models import User

def customerHome(request):
    if request.session.get('user'):
        cafes = Cafe.objects.all()
        cafe_image = []
        for cafe in cafes:
            cafe_image.append(Cafe_image.objects.filter(cafe=cafe)[0])
        
        paginator = Paginator(cafe_image, 6)

        page_number = request.GET.get('page')
        cafe_images = paginator.get_page(page_number)
        return render(request, 'customerHome.html', {'cafe': cafes, 'cafe_images': cafe_images})
    else:
        return redirect('/')


def signup(request):
    if not(request.session.get('user')):
        if request.method == 'POST':
            form = customerPostForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.check_email():
                    return render_with_error(request, 'signup.html', form, ['email'])
                if not (form.check_password1() and form.check_password()):
                    return render_with_error(request, 'signup.html', form, ['password'])
                if not form.check_phone():
                    return render_with_error(request, 'signup.html', form, ['phone'])
                
                form.save()
                # Save 성공시에는 Redirect
                request.session['user'] = request.POST.get('email')
                request.session['is_owner'] = False
                return redirect('/customer/home')
        else:
            form = customerPostForm()
            return render(request, 'signup.html', {'form': form})
    return redirect('/')

def cafeHome(request, cafeName):
    cafe = Cafe.objects.get(name=cafeName)
    
    return render(request, 'cafeHome.html', {'cafe': cafe})

def cafeReview(request):
    
    cafe_reviews = Cafe_review.objects.all()

    paginator = Paginator(cafe_reviews, 2)

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    return render(request, 'cafeReview.html', {'reviews': page_reviews})

def cafeReviewDetail(request, cafeName, reviewid):
    cafe = Cafe.objects.get(name=cafeName)
    cafe_review = Cafe_review.objects.get(cafe=cafe, review_id=reviewid)
    cafe_comment = Cafe_comment.objects.get(review=reviewid)
    
    contents = {
        'cafe_review' : cafe_review,
        'cafe_comment': cafe_comment,
        'cafeName': cafeName,
    }
    return render(request, 'cafeReviewDetail.html', {'contents': contents})

def createReview(request, cafeName):
    if request.method == 'POST':
        form = createViewForm(request.POST)
        if form.is_valid():
            cafeReview = form.save()
            cafeReview.image = request.FILES.get('image')
            cafeReview.cafe = Cafe.objects.get(name=cafeName)
            cafeReview.comment = Cafe_comment.objects.create(
                review=cafeReview,
                writer=User.objects.get(user_id=cafeReview.cafe.user)
            )
            cafeReview.writer = User.objects.get(user_id=request.session.get('user'))
            cafeReview.save()
            return redirect('/customer/'+cafeName+'/review/'+str(cafeReview.review_id))
    else:
        form = createViewForm()
        return render(request, 'cafeCreateReview.html', {'form': form})

def render_with_error(request, html, form, error_type):
    error_flg = {}
    for error in error_type:
        error_flg[error] = True
    return render(request, html, {'form': form, 'error_flg': error_flg})