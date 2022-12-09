from django import forms
from .models     import Owner
from cafe.models import Cafe,Cafe_image
import bcrypt

class loginPostForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': '이메일'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '비밀번호'}))


class signupPostForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': '이메일'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '비밀번호'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control offset-md-1',
                                                                 'placeholder': '비밀번호 확인'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '전화번호'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pe-150',
                                                         'placeholder': '카페명'}))
    human = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'maxlength': '4',
                                                                'placeholder': '최대수용인원'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                            'maxlength': '20',
                                                            'id': 'address_kakao',
                                                            'readonly':'True',
                                                            'placeholder': '주소'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'name': 'address_detail',
                                                             'placeholder':'상세 주소'}))
    

    # email이 이미 등록되었는지에 대한 validation
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Owner.objects.get(owner_id=email): # 필드에 email 값이 db에 존재하는지 확인
            raise forms.ValidationError("User already exists with that email")
        else:
            return email  # 존재하지 않는다면, 데이터를 반환
    
    # 두개의 password가 일치한지에 대한 validation 
    def clean_password1(self):
        password = self.cleaned_data.get("password") 
        password2 = self.cleaned_data.get("password2") 
        if password != password2:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    #DB에 저장
    def save(self):
        # 사장
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        phone = self.cleaned_data.get("phone")

        # 카페
        name = self.cleaned_data.get("name")
        human = self.cleaned_data.get("human")
        address = self.cleaned_data.get("address")
        datail_add = self.cleaned_data.get("datail_add")
        cafe_phone = self.cleaned_data.get("cafe_phone")

        # 카페이미지
        image = self.cleaned_data.get("image")

        make = Cafe.objects.create(
            name = name,
            max_occupancy = human,
            address = address,
            datail_add = datail_add,
            cafe_phone = cafe_phone
        )

        Owner.objects.create(           
            owner_id    = email,
            phone    = phone,
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            cafe = make.cafe_id
        )

        Cafe_image.objects.create(
            image = image,
            cafe = make.cafe_id
        )
    
    
    

