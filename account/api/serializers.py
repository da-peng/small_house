from django.contrib.auth import  get_user_model
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    CharField,
    EmailField
)

from django.core.validators import (
    validate_email
)
from django.db.models import  Q

from django.utils.translation import ugettext as _
User = get_user_model()




class  UserLoginSerializer(ModelSerializer):


    email = EmailField(label=_('邮箱')
                       ,error_messages={'required':_("邮箱内容必填"),
                                        'invalid':_("无效邮箱地址"),
                                        'blanck':_("邮箱不能为空")
                                                     })
    token = CharField(allow_blank=True,allow_null=True,required=False)\

    password = CharField(label=_('密码'))

    '''
    用户登录
    '''
    class Meta:
        model = User

        fields = [
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {
            "password":{
                "write_only":True
            }
        }



    def validate_email(self,data):
        data = self.get_initial()
        email = data.get('email')
        try:
            validate_email(email)
            return email
        except ValidationError :
            raise ValidationError(_("无效邮箱"))


    def  validate(self, data):
        user_obj = None
        email = data.get("email",None)
        password = data.get("password")
        if not email:
            raise ValidationError(_("邮箱不能为空"))
        user = User.objects.filter(
            Q(email = email)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError(_("账号或密码错误"))
        if user_obj:
            if not user_obj.check_password(password):

                raise ValidationError(_("账号或密码错误"))

        token,created = Token.objects.get_or_create(user=user_obj)

        data["token"] = token.key

        return data






class UserCreateUpdateSerializer(ModelSerializer):
    nick = CharField(label= '用户昵称')
    '''
    创建用户（注册用户），编辑用户信息
    '''
    class Meta:

        model = User
        fields = (
            'nick',
            'email',
            'phone_number',
            'password'
        )

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate_nick(self, data):# 必须要现在Serializer中定义field对象
        data = self.get_initial()
        nick = data.get('nick')
        nick_qs = User.objects.filter(nick=nick)
        if nick_qs.exists():
            raise ValidationError('用户名已存在')
        return nick


