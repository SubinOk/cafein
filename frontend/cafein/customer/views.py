import re
import json
import bcrypt
import jwt
from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
#from my_settings            import SECRET
from .models                import User

#403 오류
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

MINIMUM_PASSWORD_LENGTH = 8

def validate_email(email):
    pattern = re.compile('^.+@+.+\.+.+$') #이메일 '@'앞에는 아무 문자가 제한 없이 들어올 수 있음
    if not pattern.match(email):
        return False
    return True

def validate_password(password): # 우선 8자리 이상

    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False
    return True

def validate_phone(phone):
    pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')#'-'없이 숫자만 입력하도록 
    if not pattern.match(phone):
        return False
    return True

@method_decorator(csrf_exempt,name ='dispatch')

class SignupView(View):
    def post(self, request):

        #  if request.method == 'POST':
        #     if request.POST['password1'] == request.POST['password2']:
       

        #         data     = json.loads(request.body)
        #         user_id   = request.POST['username'],
        #         password = request.POST['password1'],
        #         name     = request.POST['name'],
        #         phone    = request.POST['phone'],
        #         gender   = request.POST['gender'],
        #         age    = request.POST['age'],

        data     = json.loads(request.body)
        user_id    = data.get('user_id', None)
        password = data.get('password', None)
        name     = data.get('name', None)
        phone    = data.get('phone', None)
        gender   = data.get('gender', None)
        age    = data.get('age', None)
       

        # KEY_ERROR check
        if not(password and user_id and password and phone):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # validation check
        if not validate_email(user_id): 

            return JsonResponse({'message': 'EMAIL_VALIDATION_ERROR'}, status=422)

        if not validate_password(password):
            return JsonResponse({'message': 'PASSWORD_VALIDATION_ERROR'}, status=422)

        if not validate_phone(phone):
            return JsonResponse({'message': 'PHONE_VALIDATION_ERROR'}, status=422)

        
        # unique check
        if User.objects.filter(Q(user_id=user_id) | Q(name=name) | Q(phone=phone)).exists():
            return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)

        User.objects.create(
            user_id    = user_id,
            name     = name,
            phone    = phone,
            gender = gender,
            age = age,
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        return JsonResponse({'message': 'SUCCESS'}, status=200)


class LoginView(View):
    def post(self, request):
        data     = json.loads(request.body)
        user_id    = data.get('user_id', None)
        password = data.get('password', None)
        
        # key error check
        if not (password and user_id):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)        
            
        # valid user check  
        if User.objects.filter(Q(user_id=user_id)).exists():
            user = User.objects.get(Q(user_id=user_id))

            # password check
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                
                # JSON Web Token
                token = jwt.encode({'user_id': user.id},  algorithm='HS256')
                #token =jwt.encode({'user_id': user.id}, SECRET['secret'], algorithm='HS256')
                return JsonResponse({'message': 'SUCCESS', 'access_token': token}, status=200) 
            
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
        
        return JsonResponse({'message': 'INVALID_USER'}, status=401)


