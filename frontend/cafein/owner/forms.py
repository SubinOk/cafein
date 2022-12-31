from django import forms
from account.models import User
from cafe.models import Cafe, Cafe_image, Cafe_menu
import bcrypt
import re

class ownerManageForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['max_occupancy', 'address', 'datail_add', 'cafe_phone']
        widgets = {
            'max_occupancy': forms.TextInput(attrs={'class': 'form-control',
                                                          'maxlength': '4',
                                                          'placeholder': '최대수용인원'}),
            'address': forms.TextInput(attrs={'class': 'form-control',
                                                            'maxlength': '20',
                                                            'id': 'address_kakao',
                                                            'readonly': 'True',
                                                            'placeholder': '주소'}),
            'datail_add': forms.TextInput(attrs={'class': 'form-control',
                                                             'name': 'address_detail',
                                                             'placeholder': '상세 주소'}),
            'cafe_phone': forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '전화번호 ("-" 없이 작성)'}),
        }

    # 카페 이미지 추가해야함 
    # image = forms.ImageField()

    # 이미지업로드 횟수 3장 제한
    # def numlimit(self):
    #     image = self.files.getlist("image")
    #     if len(image) <= 3:
    #         return True
    #     else:
    #         return False

    # 카페번호 '-'없이 숫자만 입력하도록 
    def check_cafePhone(self):
        cafe_phone = self.cleaned_data.get("cafe_phone")
        pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
        if not pattern.match(cafe_phone):
            return False
        return True

    #  카페 정보 수정 
    def cafeUpdate(self, user_id, cafe_name, images):

        # 카페정보
        name = cafe_name
        human = self.cleaned_data.get("max_occupancy")
        address = self.cleaned_data.get("address")
        address2 = self.cleaned_data.get("datail_add")
        cafe_phone = self.cleaned_data.get("cafe_phone")
        # 카페이미지
        image = images

        try:
            cafe = Cafe.objects.get(user_id=user_id)
            cafe_image = Cafe_image.objects.filter(cafe=cafe)
            if not cafe.name == name:
                cafe.name = name
            cafe.max_occupancy = human
            cafe.address = address
            cafe.datail_add = address2
            cafe.cafe_phone = cafe_phone
            cafe.save()

            for idx in range(len(image['images'])):
                if idx < len(cafe_image):
                    if not cafe_image[idx].image == image['image_names'][idx]:
                        #
                        # 입력하는 이미지들의 확장자와 크기 체크하는 부분 추가해줘야함
                        #
                        cafe_image[idx].image = image['images'][idx]
                        cafe_image[idx].cafe = cafe
                        cafe_image[idx].save()
                else:
                    if not image['images'][idx] == '':
                        #
                        # 입력하는 이미지들의 확장자와 크기 체크하는 부분 추가해줘야함
                        #
                        new_cafe_image = Cafe_image()
                        new_cafe_image.image = image['images'][idx]
                        new_cafe_image.cafe = cafe
                        new_cafe_image.save()
        except:
            return False

class ownerChangeForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호확인'}))

    class Meta:
        model = User
        fields = ['password', 'phone']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '"-"을 포함하지 않는 전화번호'}),
        }

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

    # 사장 전화번호 '-'없이 숫자만 입력하도록
    def check_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
        if not pattern.match(phone):
            return False
        return True

    def update(self, user_id):
        email = user_id
        password = self.cleaned_data.get("password")
        phone = self.cleaned_data.get("phone")
        try:
            owner = User.objects.get(user_id=email)
            owner.password =  owner.set_password(password)
            owner.phone = phone
            owner.save()
            return True
        except:
            return False


class ownerPostForm(forms.ModelForm):
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
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pe-150',
                                                         'placeholder': '카페명'}))
    human = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'maxlength': '4',
                                                          'placeholder': '최대수용인원'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'maxlength': '20',
                                                            'id': 'address_kakao',
                                                            'readonly': 'True',
                                                            'placeholder': '주소'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'name': 'address_detail',
                                                             'placeholder': '상세 주소'}))
    cafe_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': '전화번호 ("-" 없이 작성)'}))

    # 카페 이미지 추가해야함
    image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': '', 'class': 'text-gray ptd-13'}))

    # email이 이미 등록되었는지, 그리고 이메일 형식에 맞는지에 대한 validation
    def check_email(self):
        email = self.cleaned_data.get("email")
        owner = User.objects.filter(email=email).first()
        if owner is None:
            pattern = re.compile('^.+@+.+\.+.+$')  # 이메일 '@'앞에는 아무 문자가 제한 없이 들어올 수 있음
            if not pattern.match(email):
                return False
            else:
                return True  # db에 존재하지 않고, 이메일 형식이 맞다면 데이터를 반환
        else:
            # 필드에 email 값이 db에 존재하는지 확인
            return False

    # 입력한 password가 조건에 맞는지에 대한 validation
    def check_password(self):
        password = self.cleaned_data.get("password")
        # 영어,숫자,특수문자 포함하고 8~25자리수를 허용
        pattern = re.compile('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,25}$')
        if not pattern.match(password):
            return False
        else:
            return True

    # 카페 이름 같은 게 있는지 확인하기 
    def check_cafename(self):
        cafename = self.cleaned_data.get("name")
        try:
            Cafe.objects.get(name=cafename)
            return False
        except Cafe.DoesNotExist:
            return True

    # 두개의 password가 일치한지에 대한 validation 
    def check_password1(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            return False
        else:
            return True

    # 사장 전화번호 '-'없이 숫자만 입력하도록 
    def check_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
        if not pattern.match(phone):
            return False
        return True

    # 카페번호 '-'없이 숫자만 입력하도록 
    def check_cafePhone(self):
        cafe_phone = self.cleaned_data.get("cafe_phone")
        pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
        if not pattern.match(cafe_phone):
            return False
        return True

    # DB 삭제 탈퇴 회원 정보 
    def delete(self):
        email = self.cleaned_data.get("email")
        owner = User.objects.get(user_id=email)
        owner.delete()

    # 4MB 용량제한 & 확장자 제한
    def imagelimit(self):
        image = self.files.getlist("image")
        for image in image:
            if image.size < 4 * 1024 * 1024:
                image_extensions = ['.png', '.jpg', '.jpeg']
                image_lower = str(image).lower()
                is_allowed_extension = [image_extension in image_lower for image_extension in image_extensions]
                if True in is_allowed_extension:
                    return True
        return False

    # 이미지업로드 횟수 3장 제한 
    def numlimit(self):
        image = self.files.getlist("image")
        if len(image) <= 3:
            return True
        else:
            return False

    # DB에 회원가입 값 저장
    def save(self):
        # 사장
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        phone = self.cleaned_data.get("phone")

        # 카페
        name = self.cleaned_data.get("name")
        human = self.cleaned_data.get("human")
        address = self.cleaned_data.get("address")
        address2 = self.cleaned_data.get("address2")
        cafe_phone = self.cleaned_data.get("cafe_phone")

        # 카페이미지
        image = self.files.getlist("image")

        user = User(user_id=email)
        user.email = email
        user.phone = phone
        user.set_password(password)
        user.is_owner = 1
        user.save()
        make=user
    

        cafe = Cafe.objects.create(
            name=name,
            max_occupancy=human,
            address=address,
            datail_add=address2,
            cafe_phone=cafe_phone,
            user=make
        )

        for image in image:
            Cafe_image.objects.create(
                image=image,
                cafe=cafe
            )


class cafeMenuForm(forms.ModelForm):
    class Meta:
        model = Cafe_menu
        fields = ['name', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '메뉴 이름', 'maxlength': "20"}),
            'price': forms.TextInput(attrs={'type': 'number', 'class': 'form-control mt-3', 'placeholder': '가격'}),
        }

    def save(self, user_id):
        cafe = Cafe.objects.get(user_id=user_id)
        Cafe_menu.objects.create(
            cafe=cafe,
            name=self.cleaned_data.get('name'),
            image=self.cleaned_data.get("image"),
            price=self.cleaned_data.get('price'),
        )
