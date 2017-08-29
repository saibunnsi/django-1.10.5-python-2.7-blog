#coding:utf-8
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
#from .utils import code_generator
#code_generator 发送账号激活邮件待解决！
from .utils import code_generator
class MyUserManager(UserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username = username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        #只有管理员的邮箱可以发送修改密码的邮件！！！
        user.is_staff = True
        user.save(using=self._db)
        return user

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'

class MyUser(AbstractUser):
    username = models.CharField(max_length=255,
                                validators=[
                                    RegexValidator(
                                        regex=USERNAME_REGEX,
                                        message='Username must be Alpahnumeric or contain any of the following:".@+-"',
                                        code='invalid_username'
                                    )],
                                unique=True,
                                )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    zipcode = models.CharField(max_length=120, default="92660")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        #The user is identified by their email address
        return self.email
    def get_short_name(self):
        #The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the User have a specific permission?"
        #Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        #Simplest possible answer: Yes, always
        return True

class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    key = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)

def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        #send email
        print('activation created')

post_save.connect(post_save_activation_receiver, sender=ActivationProfile)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    city = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return str(self.user.username)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver,sender=settings.AUTH_USER_MODEL)
