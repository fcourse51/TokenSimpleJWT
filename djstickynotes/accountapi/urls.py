from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )

from .views import (
    user_details_api,
    user_login_api,
    user_signup_api,
    user_logout_api,
    reset_password_api
) 

urlpatterns = [
    path('user_details/', user_details_api, name='user_details_api'),
    path('login/', user_login_api, name='user_login_api'),
    path('signup/', user_signup_api, name='user_signup_api'),
    path('logout/', user_logout_api, name='user_logout_api'),
    path('reset-password/', reset_password_api, name='reset_password_api'),

]