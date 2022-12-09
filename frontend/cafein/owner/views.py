from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import loginPostForm, signupPostForm

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

# Create your views here.

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
        del(request.session['user'])

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
    if request.method == 'POST':
        form = signupPostForm(request.POST)
        if form.is_valid():
            form.save()
    else :
        form = signupPostForm()
        return render(request, 'signup.html', {'form':form})

def checkPassword(request):
    if request.session.get('user'):
        if request.method == 'POST':
            try:
                owner = get_object_or_404(Owner, owner_id=request.session.get('user'))
                if bcrypt.checkpw(request.POST.get('id_password').encode('utf-8'), owner.password.encode('utf-8')):
                    # 위의 체크를 문제없이 통과하면 이후 페이지로 전송
                    return render(request, 'ownerChange.html')
                else:
                    return render(request, 'checkPassword.html', {'flg': True})
            except:
                return redirect('/')
        else:
            return render(request, 'checkPassword.html')
    return redirect('/')

#추가부분
# def validate_email(email):
#     pattern = re.compile('^.+@+.+\.+.+$') #이메일 '@'앞에는 아무 문자가 제한 없이 들어올 수 있음
#     if not pattern.match(email):
#         return False
#     return True

# def validate_password(password): # 우선 8자리 이상

#     if len(password) < MINIMUM_PASSWORD_LENGTH:
#         return False
#     return True

# def validate_phone(phone):
#     pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')#'-'없이 숫자만 입력하도록 
#     if not pattern.match(phone):
#         return False
#     return True

# @method_decorator(csrf_exempt,name ='dispatch')

# class SignupView(View):
#     def post(self, request):

#         #카페사장
#         data = json.loads(request.body)
#         owner_id = data.get('owner_id', None)
#         password = data.get('password', None)
#         phone = data.get('phone', None)

#         cafe = request.cafe

#         #카페정보
#         Cafe.name = data.get('name', None)
#         Cafe.max_occupancy  = data.get('max_occupancy', None)
#         Cafe.address = data.get('address', None)
#         Cafe.datail_add = data.get('datail_add', None)
#         Cafe.cafe_phone = data.get('cafe_phone', None)

#         #카페이미지
#         Cafe_image.image = data.get('image_id', None)

#         Cafe_image.cafe = request.cafe

#         # KEY_ERROR check
#         if not(password and owner_id and password and phone):
#             return JsonResponse({'message': 'KEY_ERROR'}, status=400)

#         # validation check
#         if not validate_email(owner_id): 

#             return JsonResponse({'message': 'EMAIL_VALIDATION_ERROR'}, status=422)

#         if not validate_password(password):
#             return JsonResponse({'message': 'PASSWORD_VALIDATION_ERROR'}, status=422)

#         if not validate_phone(phone):
#             return JsonResponse({'message': 'PHONE_VALIDATION_ERROR'}, status=422)


#         # unique check
#         if Owner.objects.filter(Q(owner_id=owner_id)).exists():
#             return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)



#         Owner.objects.create(
#             cafe = cafe,
#             owner_id    = owner_id,
#             phone    = phone,
#             password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#         )

#         if Cafe.objects.filter(cafe_id = Cafe.cafe_id):
#             Cafe.objects.create(
#             name    = Cafe.name,
#             max_occupancy    =  Cafe.max_occupancy,
#             address =  Cafe.address,
#             datail_add = Cafe.datail_add,
#             cafe_phone = Cafe.cafe_phone
#             )


#         if Cafe_image.objects.filter(cafe_id = Cafe_image.cafe_id):
#             Cafe_image.objects.create(
#             cafe = Cafe_image.cafe,
#             image = Cafe_image.image
#             )

#         return JsonResponse({'message': 'SUCCESS'}, status=200)


# class LoginView(View):
#     def post(self, request):
#         data     = json.loads(request.body)
#         owner_id    = data.get('owner_id', None)
#         password = data.get('password', None)

#         # key error check
#         if not (password and owner_id):
#             return JsonResponse({'message': 'KEY_ERROR'}, status=400)        

#         # valid user check  
#         if Owner.objects.filter(Q(owner_id=owner_id)).exists():
#             user = Owner.objects.get(Q(owner_id=owner_id))

#             # password check
#             if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

#                 # JSON Web Token
#                 token = jwt.encode({'owner_id': owner_id},  algorithm='HS256')
#                 #token =jwt.encode({'user_id': user.id}, SECRET['secret'], algorithm='HS256')
#                 return JsonResponse({'message': 'SUCCESS', 'access_token': token}, status=200) 

#             return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

#         return JsonResponse({'message': 'INVALID_USER'}, status=401)

#
# class testSignupView():
#
#     Owner.objects.create(
#         cafe = None,
#         owner_id    = 'tunta3586@naver.com',
#         phone    = '01021354681',
#         password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#     )
