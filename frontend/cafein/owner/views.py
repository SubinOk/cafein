from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import loginPostForm, ownerPostForm, ownerChangeForm, ownerManageForm

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

#모델
from account.models import User
from cafe.models import Cafe,Cafe_image

MINIMUM_PASSWORD_LENGTH = 8


def ownerLogin(request):
    if request.method == 'POST':
        form = loginPostForm(request.POST)
        print('1')
        if form.is_valid():
            print(form.cleaned_data['email'])
            owner = User.objects.filter(email=form.cleaned_data['email']).first()
            print(form)
            print(owner)
            if owner is None:
                return render_with_error(request, 'ownerLogin.html', form, ['email'])
            if bcrypt.checkpw(form.cleaned_data['password'].encode('utf-8'), owner.password.encode('utf-8')):
                request.session['user'] = form.cleaned_data['email']
                return redirect('/owner/home')
            else:
                return render_with_error(request, 'ownerLogin.html', form, ['password'])
        else:
            print('3')
            return render_with_error(request, 'ownerLogin.html', form, ['email'])
    else:
        form = loginPostForm()
    return render(request, 'ownerLogin.html', {'form': form})


def ownerLogout(request):
    request.session.pop('user')
    return redirect('/')


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
                    print(1)
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
                return redirect('/owner/home')
        else:
            form = ownerPostForm()
            return render(request, 'signup.html', {'form': form})
    return redirect('/')


def checkPassword(request):
    if request.session.get('user'):
        if request.method == 'POST':
            owner = User.objects.filter(email=request.session.get('user')).first()
            if owner is None:
                return redirect('/')
            else:
                if bcrypt.checkpw(request.POST.get('id_password').encode('utf-8'), owner.password.encode('utf-8')):
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
        if owner is None:
            return redirect('/')
        else:
            if bcrypt.checkpw(request.POST.get('id_password').encode('utf-8'), owner.password.encode('utf-8')):
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
        form = ownerManageForm(request.POST)
        return render(request, 'ownerManage.html', {'form': form})
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