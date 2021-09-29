from django import forms
from users.models import User


class SignUpForm(forms.ModelForm):
    # User 모델의 메타데이터를 가져와서 그 중에 sign up에 필요한 form을 만듦
    class Meta:
        model = User
        fields = ("first_name", "email", "phone")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "phone": forms.NumberInput(attrs={"placeholder": "Phone Number"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    # email을 검증하기 위한 clean method override.
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # sign up시 입력한 email이 가입이 되어있으면 경고문구를 나타냄
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        # sign up시 입력한 email이 가입이 되어있지 않으면 입력 email을 반환하여 진행함
        except User.DoesNotExist:
            return email

    # password를 검증하기 위한 clean method override.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        # 입력된 password를 비교해 같지 않으면 경고문구를 나타냄.
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
            # 입력된 password가 같으면 password를 반환하여 진행함.
        else:
            return password

    def save(self):
        # db에 저장하지 않고 form 입력값을 가져옴
        user = super().save(commit=False)
        # 저장하기전 형식 유효성 검사 후 저장
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={"placeholder": "Email"},
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password"},
        ),
    )

    # email, password 각각 검증이 필요할 경우 clean method를 override 하여 세분화.
    # 각각 검증이 필요 없을 경우 override 하지 않고 clean 메소드를 호출하여 사용한다.
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            # 가입되어 있는 email과 입력된 email 비교.
            user = User.objects.get(email=email)
            # password 검증.
            if user.check_password(password):
                return self.cleaned_data
            # error를 특정 필드에서 나타나게 하기위해 add_error method 사용.
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except User.DoesNotexist:
            self.add_error("email", forms.ValidationError("User does mot exist"))
