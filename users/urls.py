from django.urls import path
from users.views import (
    LoginView,
    SignUpView,
    log_out,
    UserProfileView,
    kakao_login,
    kakao_callback,
    google_login,
    google_callback,
    naver_login,
    naver_callback,
    UpdateProfileView,
    UpdatePasswordView,
)

app_name = "users"


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", log_out, name="logout"),
    path("<int:pk>/", UserProfileView.as_view(), name="profile"),
    path("update-profile/", UpdateProfileView.as_view(), name="update"),
    path("update-password/", UpdatePasswordView.as_view(), name="password"),
    path("login/kakao/", kakao_login, name="kakao-login"),
    path("login/kakao/callback/", kakao_callback, name="kakao-callback"),
    path("login/google/", google_login, name="google-login"),
    path("login/google/callback", google_callback, name="google-callback"),
    path("login/naver/", naver_login, name="naver-login"),
    path("login/naver/callback", naver_callback, name="naver-callback"),
]
