from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import ownerPostForm, ownerChangeForm, ownerManageForm, cafeMenuForm

#403 오류해결
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#추가
import re
import json
import bcrypt
import jwt
from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.db.models       import Q
from django.core.mail.message import EmailMessage
from django.contrib.auth.hashers import check_password

#모델
from account.models import User
from cafe.models import Cafe, Cafe_image, Cafe_review, Cafe_comment, Cafe_menu, Cafe_sentiment, Cafe_rank, Cafe_wordcloud

from . import main

# 멀티프로세스
from multiprocessing import Process
import os

# 워드클라우드
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.colors import LinearSegmentedColormap

MINIMUM_PASSWORD_LENGTH = 8


def ownerHome(request):
    if request.session.get('user'):
        try: 
            cafe = Cafe.objects.get(user = request.session.get('user'))
            cafe_sentiment = Cafe_sentiment.objects.get(cafe = cafe)
            cafe_rank = Cafe_rank.objects.filter(sentiment=cafe_sentiment.sentiment_id).order_by('rank')
            cafe_reviews = Cafe_review.objects.filter(cafe=cafe).order_by('-date')[:3]
            return render(request, 'ownerHome.html', {'cafe_sentiment':cafe_sentiment, 'cafe':cafe, 'reviews': cafe_reviews
                                                    ,'cafe_rank': cafe_rank, 'title': '사장 홈',})
        except:
            cafe = Cafe.objects.get(user = request.session.get('user'))
            return render(request,'ownerHome2.html', {'cafe': cafe, 'title': '리뷰 분석중',})
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
                    return render_with_error(request, 'signup.html', form, ['email'], '사장 회원가입')
                if not (form.check_password1() and form.check_password()):
                    return render_with_error(request, 'signup.html', form, ['password'], '사장 회원가입')
                if not form.check_phone():
                    return render_with_error(request, 'signup.html', form, ['phone'], '사장 회원가입')
                if not form.check_cafename():
                    return render_with_error(request, 'signup.html', form, ['name'], '사장 회원가입')
                if not form.check_cafePhone():
                    return render_with_error(request, 'signup.html', form, ['cafephone'], '사장 회원가입')
                if not form.imagelimit():
                    return render_with_error(request, 'signup.html', form, ['image'], '사장 회원가입')
                if not form.numlimit():
                    return render_with_error(request, 'signup.html', form, ['imagelimit'], '사장 회원가입')
                
                name = form.cleaned_data.get("name")
                phone = form.cleaned_data.get("cafe_phone")
                
                form.save()
                # Save 성공시에는 Redirect
                request.session['user'] = request.POST.get('email')
                request.session['is_owner'] = True
                
                proc = Process(target=main.crawl, args=(name,phone))
                proc.start()
                
                return redirect('/owner/home')
        else:
            form = ownerPostForm()
            return render(request, 'signup.html', {'form': form, 'title': '사장 회원가입'})
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
                    return redirect('/owner/change')
                else:
                    return render_with_error(request, 'checkPassword.html', '', ['password'], {'title': '비밀번호 확인'})
        else:
            return render(request, 'checkPassword.html', {'title': '비밀번호 확인'})
    return redirect('/')


def ownerChange(request):
    if request.session.get('user'):
        if request.method == 'POST':
            user_id = request.session.get('user')
            form = ownerChangeForm(request.POST)
            if form.is_valid(): #is_valid 필수로 쓰기
                if not (form.check_password() and form.check_password1()):
                    return render_with_error(request, 'ownerChange.html', form, ['password'], '회원 정보 수정')
                if not form.check_phone():
                    return render_with_error(request, 'ownerChange.html', form, ['phone'], '회원 정보 수정')
                form.update(user_id)
            return redirect('/owner/home/')
        else:
            form = ownerChangeForm()
            return render(request, 'ownerChange.html', {'form': form, 'title': '회원 정보 수정'})
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
                request.session.flush() 
                return redirect('/')
            else:
                return render_with_error(request, 'ownerDelete.html', '', ['password'], {'title': '탈퇴하기'})
    else:
        return render(request, 'ownerDelete.html', {'title': '탈퇴하기'})


def render_with_error(request, html, form, error_type, title=''):
    error_flg = {}
    for error in error_type:
        error_flg[error] = True
    return render(request, html, {'form': form, 'error_flg': error_flg, 'title': title})
        

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
                if not form.check_cafePhone():
                    return render_with_error(request, 'ownerManage.html', form, ['cafephone'], '카페 관리')
                form.cafeUpdate(request.session.get('user'), cafe_name, update_image)
            return redirect('/owner/home')
        else:
            cafeform = Cafe.objects.filter(user_id=request.session.get('user'))
            imageform = Cafe_image.objects.filter(cafe_id=cafeform[0].cafe_id)
            form = ownerManageForm(instance=cafeform[0])
            return render(request, 'ownerManage.html', {'form': form, 'cafe_name': cafeform[0].name, 'imageform': imageform, 'title': '카페 관리'})
    else:
        return redirect('/')

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
            return render(request, 'ownerChange.html', {'title': '회원 정보 수정'})
    else:
        return redirect('/')


def ownerStatistics(request):
    if request.session.get('user'):
        data = request.GET.get('data')
        if data is None:
            data = "price"
        cafe = Cafe.objects.get(user = request.session.get('user'))
        cafe_sentiment = Cafe_sentiment.objects.get(cafe = cafe)
        cafe_rank = Cafe_rank.objects.filter(sentiment=cafe_sentiment.sentiment_id).order_by('rank_id')
            
        return render(request, 'ownerStatistics.html', {'data': data, 'cafe_rank': cafe_rank, 'cafe_name': cafe.name, 'title': '고객 통계'})
    else:
        return redirect('/')


def ownerComent(request):
    cafe_reviews = Cafe_review.objects.filter(cafe=Cafe.objects.get(user_id=request.session.get('user'))).order_by('-date')

    paginator = Paginator(cafe_reviews, 2)

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    return render(request, 'ownerComent.html', {'reviews': page_reviews, 'title': '리뷰 게시판'})


def ownerComentDetail(request, reviewid):
    cafe_review = Cafe_review.objects.get(review_id=reviewid)
    cafe_comment = Cafe_comment.objects.get(review=cafe_review.review_id)
    
    contents = {
        'cafe_review' : cafe_review,
        'cafe_comment': cafe_comment,
    }
    
    return render(request, 'ownerComentDetail.html', {'contents': contents, 'title': '리뷰 게시판'})


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
    if request.session.get('user'):
        if request.method == 'POST':
            if request.POST.get('menuList') is None:
                form = cafeMenuForm(request.POST, request.FILES)
                if form.is_valid():
                    if not form.check_menuname():
                        result = {'result': False, 'error': 'name'}
                        return JsonResponse({'result': result})
                    if not form.imagelimit():
                        result = {'result': False, 'error': 'image'}
                        return JsonResponse({'result': result})
                    form.save(request.session.get('user'))
                    return JsonResponse({'result': True})
                return JsonResponse({'result': False})
            else:
                menu_list = request.POST.get('menuList').split(',')
                cafe = Cafe.objects.filter(user_id=request.session.get('user'))
                for menu in menu_list:
                    cafe_menu = Cafe_menu.objects.filter(cafe=cafe[0], name=menu)
                    cafe_menu[0].delete()

                return JsonResponse({'result': True})

        elif request.method == 'GET':
            user_id = request.session.get('user')
            cafe = Cafe.objects.filter(user=User.objects.filter(user_id=user_id)[0])
            cafe_menu = Cafe_menu.objects.filter(cafe=cafe[0])
            menu_form = cafeMenuForm()
            return render(request, 'ownerManageMenu.html', {'cafe_menu': cafe_menu, 'menu_form': menu_form, 'title': '카페 관리'})
    else:
        return redirect('/')
    
    
def checkCafeData(request):
    cafe = Cafe.objects.get(cafe_id=request.GET.get('cafe_id'))
    cafe_sentiment = Cafe_sentiment.objects.filter(cafe=cafe)
    if len(cafe_sentiment) == 1:
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})