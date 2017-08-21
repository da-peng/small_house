# encoding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager
)
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from django.contrib.auth.hashers import make_password

import hashlib

class UserManager(BaseUserManager):

    def create_user(self, email,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('请输出邮箱地址')

        user = self.model(
            email=email,
        )

        m = hashlib.md5()

        m.update(password.encode('utf-8'))

        password_md5 = str(m.hexdigest())

        user.set_password(password_md5) # 将用户的密码的MD5 再使用django的加密规则存储

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password= password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    uid = models.AutoField(
        verbose_name='用户uid',
        primary_key=True,
    )
    nick = models.CharField(
        verbose_name='用户昵称',
        max_length=255,
        unique=True,
        null= True
    )
    email = models.EmailField(
        verbose_name='注册邮箱',
        max_length=255,
        unique=True,
        null=True,
        # error_messages="无效邮箱地址",
        error_messages={'invalid': _("无效邮箱地址")}
    )

    phone_number = models.IntegerField(
        verbose_name='注册手机号',
        unique=True,
        null=True,
    )

    face_image = models.ImageField(
        upload_to='Images/',
        default='Images/None/default-img.jpg',#设置默认用户头像
    )

    # content = models.TextField(null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The users is identified by their email address
        return self.email

    def get_short_name(self):
        # The users is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the users have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the users have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the users a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # def get_markdown(self):
    #     content = self.content
    #     markdown_text = markdown(content)
    #     return mark_safe(markdown_text)




    # def get_absolute_url(self):
    #     return reverse('user-api:detail',kwargs={'nick':self.nick})


# class Employee(models.Model):
#     users = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.CharField(
#         verbose_name='部门',
#         max_length=100,
#     )


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

