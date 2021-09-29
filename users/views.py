import os
import requests
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import User
from users.forms import LoginForm, SignUpForm
from users.mixins import LoggedOutOnlyView, LoggedInOnlyView, EmailLoginOnlyView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView

# from django.core.files.base import ContentFile


# Create your views here.

# FormView를 Inheritance한 sign up view class.
class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("core:home")

    # is_valid override, form에 대한 검증 메소드 정의, 유효한 경우 success_url로 redirect.
    def form_valid(self, form):

        # form에서 입력된 값을 저장함.
        form.save()

        # clean method을 거친 form의 입력값이 유효하다면(True) 그 값이 cleaned_data에 저장됨.
        # cleaned_data에 저장된 email, password 가져옴.
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        # username과 password를 backend에서 자격 증명을 확인하여 유효한 경우 user object를 반환함.
        user = authenticate(self.request, username=email, password=password)

        # 검증된 user object의 로그인 실행.
        # form_valid 메소드는 overriding 되었기 때문에 success_url로 redirect 할 수 없음.
        # 때문에 super() 함수로 부모 FormView의 form_valid 메소드를 실행시킴.
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LoginView(LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = LoginForm

    def form_valid(self, form):

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    # FormView의 get_success_url를 override.
    # 사용자가 특정 페이지에 갈려다가 로그인을 하게 된다면 로그인시 들어갈려던 페이지로 redirect
    def get_success_url(self):
        # request.GET.get으로 들어갈려던 "?next=???"을 가져온다
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class UserProfileView(DetailView):

    model = User
    context_object_name = "user_obj"


class UpdateProfileView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "birthdate",
        "phone",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        print(self.request.user.login_method)
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["phone"].widget.attrs = {"placeholder": "Phone Number"}

        return form


class UpdatePasswordView(
    EmailLoginOnlyView,
    LoggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }

        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_REST_API_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_REST_API_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://Kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&{redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com//v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        print(profile_json)
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        if properties is not None:
            nickname = properties.get("nickname")
        else:
            nickname = kakao_account.get("profile").get("nickname")

        # profile_image = kakao_account.get("profile").get("profile_image_url")

        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except User.DoesNotExist:
            user = User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

            """
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
            """

        messages.success(request, f"welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class GoogleException(Exception):
    pass


def google_login(request):
    client_id = os.environ.get("GOOGLE_OAUTH2_ID")
    scope = "email"
    # 프로필 api 연결 할 것
    redirect_uri = "http://127.0.0.1:8000/users/login/google/callback"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
    )


def google_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GOOGLE_OAUTH2_ID")
        client_secret = os.environ.get("GOOGLE_OAUTH2_PASSWORD")
        redirect_uri = "http://127.0.0.1:8000/users/login/google/callback"

        if code is not None:
            token_request = requests.post(
                f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GoogleException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                email_request = requests.get(
                    f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                email_json = email_request.json()
                email = email_json.get("email")
                print(email_json)
                if email is not None:
                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_GOOGLE:
                            raise GoogleException(
                                f"Please log in with: {user.login_method}"
                            )
                    except User.DoesNotExist:
                        user = User.objects.create(
                            email=email,
                            username=email,
                            login_method=User.LOGIN_GOOGLE,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GoogleException("Can't get your profile")
        else:
            raise GoogleException("Can't get code")
    except GoogleException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class NaverException(Exception):
    pass


def naver_login(request):
    client_id = os.environ.get("NAVER_OAUTH2_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback"
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&state=STATE_STRING&redirect_uri={redirect_uri}"
    )


def naver_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("NAVER_OAUTH2_ID")
        client_secret = os.environ.get("NAVER_OAUTH2_PASSWORD")
        redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback"

        if code is not None:
            token_request = requests.post(
                f"https://nid.naver.com/oauth2.0/token?&client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise NaverException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://openapi.naver.com/v1/nid/me",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                print(profile_json)
                email = profile_json.get("response").get("email")
                name = profile_json.get("response").get("name")
                # profile_image = profile_json.get("response").get("profile_image")
                if email is not None:
                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_NAVER:
                            raise NaverException(
                                f"Please log in with: {user.login_method}"
                            )
                    except User.DoesNotExist:
                        user = User.objects.create(
                            email=email,
                            username=email,
                            first_name=name,
                            login_method=User.LOGIN_NAVER,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise NaverException("Can't get your profile")
        else:
            raise NaverException("Can't get code")
    except NaverException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
