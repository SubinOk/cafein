from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import resolve_url
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.http import HttpResponse
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
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _

from owner.models import Owner

UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

# Create your views here.
def mainPage(request):
    if request.session.get('user'):
        return redirect('/owner/home')
    return render(request, 'mainPage.html')

def login(request):
    return render(request, 'login.html')

# 비밀번호 재설정
class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html' 
    success_url = reverse_lazy('main:password_reset_done')
    def form_valid(self, form):
        if Owner.objects.filter(email=self.request.POST.get("email")).exists():
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
    form_class = SetPasswordForm
    success_url=reverse_lazy('main:password_reset_confirm')
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context
    