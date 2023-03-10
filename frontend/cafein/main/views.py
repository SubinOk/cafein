from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from main.forms import UserSetPasswordForm
from .forms import UserloginPostForm

from owner.views import render_with_error

from account.models import User
from cafe.models import Cafe, Cafe_image, Cafe_congestion

UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

# 비밀번호 재설정
class UserPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    template_name = 'password_reset.html' 
    success_url = reverse_lazy('main:password_reset_done')
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset_done_fail.html')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    success_url=reverse_lazy('main:password_reset_complete')
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


# Create your views here.
def mainPage(request):
    if request.session.get('is_owner'):
        if request.session['is_owner'] == True:
            return redirect('/owner/home')
        else:
            return redirect('/customer/home')
    return render(request, 'mainPage.html',{'main': 'main', 'title': '메인 홈'})

# 로그인
def login(request):
    if request.method == 'POST':
        form = UserloginPostForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            password = form.cleaned_data['password']
            if user is None:
                return render_with_error(request, 'login.html', form, ['email'])
            if  check_password(password, user.password):
                request.session['user'] = form.cleaned_data['email']
                # 사장
                if user.is_owner == True:
                    request.session['is_owner'] = user.is_owner
                    return redirect('/owner/home')
                # 고객
                else:
                    request.session['is_owner'] = user.is_owner
                    return redirect('/customer/home')
            else:
                return render_with_error(request, 'login.html', form, ['password'])
        else:
            return render_with_error(request, 'login.html', form, ['email'])
    else:
        form = UserloginPostForm()
    return render(request, 'login.html', {'form': form})

# signup select
def singup(request):
    return render(request, 'signup_select.html')

def logout(request):
    request.session.flush() 
    return redirect('/')

def search(request):
    query = request.GET.get('search')
    cafes = Cafe.objects.filter(name__contains=query)
    cafe_content = []
    customer = User.objects.filter(email=request.session.get('user'))[0]
    for cafe in cafes:
        cafe_data = {
            'cafe': cafe,
            'cafe_image': Cafe_image.objects.filter(cafe=cafe)[0],
            'cafe_congestion': Cafe_congestion.objects.get(cafe=cafe).congestion
        }
        
        print(cafe_data)
        cafe_content.append(cafe_data)
    
    results={
        'cafe_content': cafe_content,
        'search_word': query,
        'search_cnt': len(cafes),
    }
    return render(request, 'search.html', {'results': results, 'customer': customer})