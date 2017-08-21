from django.conf.urls import  url


from .views import (
    UserLoginAPIView,
    UserCreateAPIView,
)

from django.views.generic import TemplateView
from rest_framework.authtoken import views

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name="account/page_user_login.html")),
    url(r'^login$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$',UserCreateAPIView.as_view(),name='register'),
# url(r'^api-token-auth/', views.obtain_auth_token),

]