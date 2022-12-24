from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import ownerPostForm, ownerChangeForm, ownerManageForm

#403 오류해결
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#추가
import re
import json
import bcrypt
import jwt
from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from django.core.mail.message import EmailMessage
from django.contrib.auth.hashers import check_password

#모델
from account.models import User
from cafe.models import Cafe,Cafe_image, Cafe_review, Cafe_comment

MINIMUM_PASSWORD_LENGTH = 8


def ownerHome(request):
    if request.session.get('user'):
        return render(request, 'ownerHome.html')
    else:
        return redirect('/')


def signup(request):
    # 등록된 이메일, 이메일 형식 확인
    # 두개의 password가 일치한지에 대한 validation
    # 영어(대소문자), 숫자, 특수문자 포함하고 8~25자리수를 허용
    # 전화번호 '-'없이 숫자만 입력하도록
    # 카페 이름 같은 게 있는지 확인하기
    # 전화번호 '-'없이 숫자만 입력하도록 
    # 4MB 용량제한 & 확장자 제한
    if not(request.session.get('user')):
        if request.method == 'POST':
            form = ownerPostForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.check_email():
                    return render_with_error(request, 'signup.html', form, ['email'])
                if not (form.check_password1() and form.check_password()):
                    return render_with_error(request, 'signup.html', form, ['password'])
                if not form.check_phone():
                    return render_with_error(request, 'signup.html', form, ['phone'])
                if not form.check_cafename():
                    return render_with_error(request, 'signup.html', form, ['name'])
                if not form.check_cafePhone():
                    return render_with_error(request, 'signup.html', form, ['cafephone'])
                if not form.imagelimit():
                    return render_with_error(request, 'signup.html', form, ['image'])
                if not form.numlimit():
                    return render_with_error(request, 'signup.html', form, ['imagelimit'])
                
                form.save()
                # Save 성공시에는 Redirect
                request.session['user'] = request.POST.get('email')
                request.session['is_owner'] = True
                return redirect('/owner/home')
        else:
            form = ownerPostForm()
            return render(request, 'signup.html', {'form': form})
    return redirect('/')


def checkPassword(request):
    if request.session.get('user'):
        if request.method == 'POST':
            owner = User.objects.filter(email=request.session.get('user')).first()
            password = request.POST.get('id_password')
            if owner is None:
                return redirect('/')
            else:
                if check_password(password, owner.password):
                    # 위의 체크를 문제없이 통과하면 이후 페이지로 전송
                    form = ownerChangeForm()
                    return redirect('/owner/change', {'form': form})
                else:
                    return render_with_error(request, 'checkPassword.html', '', ['password'])
        else:
            return render(request, 'checkPassword.html')
    return redirect('/')


def ownerChange(request):
    if request.session.get('user'):
        if request.method == 'POST':
            user_id = request.session.get('user')
            form = ownerChangeForm(request.POST)
            if form.is_valid(): #is_valid 필수로 쓰기
                if not (form.check_password() and form.check_password1()):
                    return render_with_error(request, 'ownerChange.html', form, ['password'])
                if not form.check_phone():
                    return render_with_error(request, 'ownerChange.html', form, ['phone'])
                form.update(user_id)
            return redirect('/owner/home/')
        else:
            form = ownerChangeForm()
            return render(request, 'ownerChange.html', {'form': form})
    else:
        return redirect('/')


def ownerDelete(request):
    if request.method == 'POST':
        if not request.session.get('user'):
            return redirect('/')
        owner = User.objects.filter(email=request.session.get('user')).first()
        password = request.POST.get('id_password')
        if owner is None:
            return redirect('/')
        else:
            if check_password(password, owner.password):
                # 위의 체크를 문제없이 통과하면 이후 페이지로 전송
                owner.delete()
                request.session.pop('user')
                return redirect('/')
            else:
                return render_with_error(request, 'ownerDelete.html', '', ['password'])
    else:
        return render(request, 'ownerDelete.html')


def render_with_error(request, html, form, error_type):
    error_flg = {}
    for error in error_type:
        error_flg[error] = True
    return render(request, html, {'form': form, 'error_flg': error_flg})
        

def ownerManage(request):
    if request.session.get('user'):
        if request.method == 'POST':
            form = ownerManageForm(request.POST)

            cafe_name = request.POST.get('name')
            image_name_1 = request.POST.get('image_name_1', '')
            image_name_2 = request.POST.get('image_name_2', '')
            image_name_3 = request.POST.get('image_name_3', '')
            image_1 = request.FILES.get('image_1', '')
            image_2 = request.FILES.get('image_2', '')
            image_3 = request.FILES.get('image_3', '')
            image_names = [image_name_1, image_name_2, image_name_3]
            images = [image_1, image_2, image_3]
            update_image = {
                'image_names': image_names,
                'images': images,
            }
            if form.is_valid():
                form.cafeUpdate(request.session.get('user'), cafe_name, update_image)
            return redirect('/owner/home')
        else:
            cafeform = Cafe.objects.filter(user_id=request.session.get('user'))
            imageform = Cafe_image.objects.filter(cafe_id=cafeform[0].cafe_id)
            form = ownerManageForm(instance=cafeform[0])
            return render(request, 'ownerManage.html', {'form': form, 'cafe_name': cafeform[0].name, 'imageform': imageform})
    else:
        return redirect('/')

#수정 중 
def cafeUpdate(request):
    if request.session.get('user'):
        if request.method == 'POST': 
            user_id=request.session.get('user')
            form = ownerManageForm(request.POST)
            if form.is_valid(): 
                form.cafeUpdate(user_id)
                form.imageUpdate(user_id)
            return redirect('/owner/home/')
        else:
            return render(request, 'ownerChange.html')
    else:
        return redirect('/')


def ownerStatistics(request):
    if request.session.get('user'):
        return render(request, 'ownerStatistics.html')
    else:
        return redirect('/')


def ownerStatisticsDetail(request):
    return render(request, 'ownerStatisticsDetail.html')


def ownerComent(request):
    return render(request, 'ownerComent.html')


def ownerComentDetail(request, reviewid):
    cafe_review = Cafe_review.objects.get(review_id=reviewid)
    cafe_comment = Cafe_comment.objects.get(review=cafe_review.review_id)
    
    contents = {
        'cafe_review' : cafe_review,
        'cafe_comment': cafe_comment,
    }
    
    return render(request, 'ownerComentDetail.html', {'contents': contents})


def ownerCommentUpload(request):
    if request.method == 'POST':
        review_comment = request.POST.get('review-comment')
        comment_id = request.POST.get('comment-id')
        cafe_comment = Cafe_comment.objects.get(comment_id=comment_id)
        cafe_comment.content = review_comment
        cafe_comment.save()
        
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})


def ownerManageMenu(request):
    return render(request, 'ownerManageMenu.html')