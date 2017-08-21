from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from django.contrib.auth import  get_user_model
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.views import APIView

from .serializers import (
    UserLoginSerializer,
    UserCreateUpdateSerializer
)

from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication
)
User = get_user_model()

# 登录

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer = UserLoginSerializer

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer(data = data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data

            token = new_data['token']

            return Response(data={
                'ret':'0',
                'msg':'登录成功'},headers= {'Authorization':'Token '+token
                                        },status=HTTP_200_OK)

        return Response(serializer.error_messages,status=HTTP_400_BAD_REQUEST)


class UserCreateAPIView(CreateAPIView):
    '''
    创建用户
    '''
    authentication_classes = (TokenAuthentication,) # 认证 必须是一个tuple 必须加一个逗号就可以了

# 以下要注意三个概念：以下三个概念是有区别的，实现方式和原理都是不一致的，虽然都有token

# 授权 Authorization

# 认证 Authentication

# csrfToken django 跨站点攻击防御手段

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer


class UserDetailAPIView(CreateAPIView):
    '''
    用户详情
    '''
    pass

# class User

# class HomePageAPIView()