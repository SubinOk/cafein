from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import resolve_url
from django.conf import settings
from django.urls import reverse_lazy

from main.forms import UserSetPasswordForm
from owner.views import render_with_error
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

from django.utils.translation import gettext_lazy as _

from account.models import User

from .forms import UserloginPostForm

import bcrypt




UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

# Create your views here.
def mainPage(request):
    if request.session.get('user'):
        return redirect('/owner/home')
    return render(request, 'mainPage.html')


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
    
# 로그인
def login(request):
    if request.method == 'POST':
        form = UserloginPostForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user is None:
                return render_with_error(request, 'login.html', form, ['email'])
            if bcrypt.checkpw(form.cleaned_data['password'].encode('utf-8'), user.password.encode('utf-8')):
                request.session['user'] = form.cleaned_data['email']
                # 사장
                if user.is_owner == True:
                    return redirect('/owner/home')
                # 고객
                else:
                    return redirect('/customer/home')
            else:
                return render_with_error(request, 'login.html', form, ['password'])
        else:
            return render_with_error(request, 'login.html', form, ['email'])
    else:
        form = UserloginPostForm()
    return render(request, 'login.html', {'form': form})


def ownerLogout(request):
    request.session.pop('user')
    return redirect('/')