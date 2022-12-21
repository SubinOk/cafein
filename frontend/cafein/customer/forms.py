from django import forms
from account.models import User
import bcrypt
import re

class customerPostForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone']
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '"-"을 포함하지 않는 전화번호'}),
        }
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control offset-md-1',
                                                                  'placeholder': '비밀번호 확인'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '전화번호 ("-" 없이 작성)'}))
    

    # 입력한 password가 조건에 맞는지에 대한 validation
    def check_password(self):
        password = self.cleaned_data.get("password")
        # 영어,숫자,특수문자 포함하고 8~25자리수를 허용
        pattern = re.compile('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,25}$')
        if not pattern.match(password):
            return False
        else:
            return True


    # 두개의 password가 일치한지에 대한 validation 
    def check_password1(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            return False
        else:
            return True

    # DB 삭제 탈퇴 회원 정보 
    def delete(self):
        email = self.cleaned_data.get("email")
        owner = User.objects.get(user_id=email)
        owner.delete()

    # DB에 회원가입 값 저장
    def save(self):
        # 사장
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        phone = self.cleaned_data.get("phone")

        User.objects.create(
            user_id=email,
            email=email,
            phone=phone,
            password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        )

        
