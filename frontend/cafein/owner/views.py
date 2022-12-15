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
from .models     import Owner
from cafe.models import Cafe,Cafe_image

MINIMUM_PASSWORD_LENGTH = 8


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
            return render(request, 'ownerHome.html', {'form': form})
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
        return render(request, 'ownerHome.html')
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
    # 등록된 이메일, 이메일 형식 확인
    # 두개의 password가 일치한지에 대한 validation
    # 영어(대소문자), 숫자, 특수문자 포함하고 8~25자리수를 허용
    # 전화번호 '-'없이 숫자만 입력하도록
    # 카페 이름 같은 게 있는지 확인하기
    # 전화번호 '-'없이 숫자만 입력하도록 
    # 4MB 용량제한 & 확장자 제한
    error_flg = {
        'email': False,
        'password': False,
        'phone': False,
        'cafename': False,
        'cafephone': False,
        'image': False,
    }
    if not(request.session.get('user')):
        if request.method == 'POST':
            form = ownerPostForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.check_email():
                    error_flg['email'] = True
                    return render(request, 'signup.html', {'form': form, 'error_flg': error_flg})
                if not (form.check_password1() and form.check_password()):
                    error_flg['password'] = True
                    return render(request, 'signup.html', {'form': form, 'error_flg': error_flg})
                # if not form.check_phone():
                #     error_flg['phone'] = True
                #     return render(request, 'signup.html', {'form':form, 'error_flg': error_flg})
                # if not form.check_cafename():
                #     error_flg['cafename'] = True
                #     return render(request, 'signup.html', {'form':form, 'error_flg': error_flg})
                # if not form.check_phone():
                #     error_flg['cafephone'] = True
                #     return render(request, 'signup.html', {'form':form, 'error_flg': error_flg})
                # if not form.imagelimit():
                #     error_flg['image'] = True
                #     return render(request, 'signup.html', {'form':form, 'error_flg': error_flg})
                
                form.save()
                # Save 성공시에는 Redirect 방식이 좀더 좋아보임
                request.session['user'] = request.POST.get('email')
                return render(request, 'ownerHome.html')
            else:
                return render(request, 'signup.html', {'form':form, 'error_flg': error_flg})
            
        else :
            form = ownerPostForm()
            return render(request, 'signup.html', {'form':form})

    return render(request, 'ownerHome.html')


def checkPassword(request):
    if request.session.get('user'):
        if request.method == 'POST':
            try:
                owner = get_object_or_404(Owner, owner_id=request.session.get('user'))
                if bcrypt.checkpw(request.POST.get('id_password').encode('utf-8'), owner.password.encode('utf-8')):
                    # 위의 체크를 문제없이 통과하면 이후 페이지로 전송
                    form = ownerChangeForm()
                    return render(request, 'ownerChange.html', {'form': form})
                else:
                    return render(request, 'checkPassword.html', {'flg': True})
            except:
                return redirect('/')
        else:
            return render(request, 'checkPassword.html')
    return redirect('/')


def ownerChange(request):
    if request.session.get('user'):
        form = ownerChangeForm()
        return render(request, 'ownerChange.html', {'form': form})
    else:
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
            return redirect('/owner/home/')
        else:
            return render(request, 'ownerChange.html')
    else:
        return redirect('/')
        

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
            owner_id=request.session.get('user')
            form = ownerManageForm(request.POST)
            if form.is_valid(): #is_valid 필수로 쓰기 
                form.cafeUpdate(owner_id)
                form.imageUpdate(owner_id)
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