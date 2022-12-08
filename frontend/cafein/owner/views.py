from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import loginPostForm


# Create your views here.

def ownerLogin(request):
    if request.method == 'POST':
        form = loginPostForm()
        return render(request, 'ownerLogin.html', {'form': form, 'flg': True})
    else:
        form = loginPostForm()
        return render(request, 'ownerLogin.html', {'form': form, 'flg': False})


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
    return render(request, 'signup.html')
