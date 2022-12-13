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

#모델
from .models     import Owner
from cafe.models import Cafe,Cafe_image

MINIMUM_PASSWORD_LENGTH = 8

changeSideBar=['회원 정보 수정', '카페 관리']
homeSideBar=['Home','리뷰 확인', '고객 통계']


def ownerLogin(request):
    if request.method == 'POST':
        form = loginPostForm(request.POST)
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        error_flg = {
            'email': False,
            'password': False
        }

        # 서버로 들어온 데이터가 비어있는지 확인
        if (email == "") or (password == ""):
            error_flg['email'] = True
            error_flg['password'] = True
            return render(request, 'ownerLogin.html', {'form': form, 'error_flg': error_flg})
        try:
            owner = get_object_or_404(Owner, owner_id=email)
        except:
            # DB에 해당 이메일이 존재하지 않았을때 return
            error_flg['email'] = True
            return render(request, 'ownerLogin.html', {'form': form, 'error_flg': error_flg})

        if bcrypt.checkpw(password.encode('utf-8'), owner.password.encode('utf-8')):
            # 위의 체크를 문제없이 통과하면 이후 페이지로 전송
            request.session['user'] = email
            return render(request, 'ownerHome.html', {'form': form, 'side': homeSideBar, 'side_select': 'Home'})
        else:
            # 입력한 encoding 패스워드가 불일치 할때 return
            error_flg['password'] = True
            return render(request, 'ownerLogin.html', {'form': form, 'error_flg': error_flg})
    else:
        form = loginPostForm()
        return render(request, 'ownerLogin.html', {'form': form})


def ownerLogout(request):
    if request.session.get('user'):
        request.session.pop('user')

    return redirect('/')


def ownerHome(request):
    if request.session.get('user'):
        return render(request, 'ownerHome.html', {'side': homeSideBar, 'side_select': 'Home'})
    else:
        return redirect('/')


def findPassword(request):
    if request.method == 'POST':

        # 일치 하는 이메일이 있는 경우 이메일 전송 방법 setting은 cafein settings.py 참조
        # to_email = 'tunta3586@gmail.com'
        # send_email = EmailMessage('Subject here', 'Here is the message', to=[to_email])
        # send_email.send()
        return render(request, 'findPassword.html', {'flg': True})
    else:
        return render(request, 'findPassword.html', {'flg': False})

def signup(request):
    if not(request.session.get('user')):
        if request.method == 'POST':
            form = ownerPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            request.session['user'] = request.POST.get('email')
            return render(request, 'ownerHome.html', {'side': homeSideBar, 'side_select': 'Home'})
        else :
            form = ownerPostForm()
            return render(request, 'signup.html', {'form':form})

    return render(request, 'ownerHome.html', {'side': homeSideBar, 'side_select': 'Home'})


def checkPassword(request):
    if request.session.get('user'):
        if request.method == 'POST':
            try:
                owner = get_object_or_404(Owner, owner_id=request.session.get('user'))
                if bcrypt.checkpw(request.POST.get('id_password').encode('utf-8'), owner.password.encode('utf-8')):
                    # 위의 체크를 문제없이 통과하면 이후 페이지로 전송
                    form = ownerChangeForm()
                    return render(request, 'ownerChange.html', {'form': form, 'side': changeSideBar, 'side_select': '회원 정보 수정'})
                else:
                    return render(request, 'checkPassword.html', {'flg': True})
            except:
                return redirect('/')
        else:
            return render(request, 'checkPassword.html')
    return redirect('/')


def ownerDelete(request):
    if request.method == 'POST':
        try:
            owner = get_object_or_404(Owner, owner_id=request.session.get('user'))
            if bcrypt.checkpw(request.POST.get('id_password').encode('utf-8'), owner.password.encode('utf-8')):
                # 위의 체크를 문제없이 통과하면 이후 페이지로 전송
                owner.delete()
                request.session.pop('user')
                return redirect('/')
            else:
                return render(request, 'ownerDelete.html', {'flg': True})
        except:
            return redirect('/')
    else:
        return render(request, 'ownerDelete.html')


def ownerUpdate(request):
    if request.session.get('user'):
        if request.method == 'POST': 
            owner_id=request.session.get('user')
            form = ownerChangeForm(request.POST)
            if form.is_valid(): #is_valid 필수로 쓰기 
                form.update(owner_id)
            return redirect('/owner/home/', {'side': homeSideBar})
        else:
            return render(request, 'ownerChange.html', {'side': homeSideBar})
    else:
        return redirect('/')
        

def ownerManage(request):
    if request.session.get('user'):
        form = ownerManageForm(request.POST)
        return render(request, 'ownerManage.html', {'form': form,'side': homeSideBar})
    else:
        return render(request, 'ownerManage.html')
#수정 중 
def cafeUpdate(request):
    if request.session.get('user'):
        if request.method == 'POST': 
            owner_id=request.session.get('user')
            form = ownerManageForm(request.POST)
            if form.is_valid(): #is_valid 필수로 쓰기 
                form.update(owner_id)
                form.imageUpdate(owner_id)
            return redirect('/owner/home/', {'side': homeSideBar})
        else:
            return render(request, 'ownerChange.html', {'side': homeSideBar})
    else:
        return redirect('/')
        
            
        

  
