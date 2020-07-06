from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,PermissionsMixin,BaseUserManager
from django.conf import settings
class NewUser(UserManager):
    def __init__(self):
        UserManager.__init__(self)

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        # username = self.model.normalize_username(username)
        user = self.model(username=username,  **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=32,unique=True,null=False)
    is_superuser = models.BooleanField(null=False,default=False)
    is_active = models.BooleanField(null=False,default=False)
    is_staff = models.BooleanField(null=False,default=False)
    mode =  models.CharField(max_length=32,null=True)
    number = models.IntegerField(null=True)
    target = models.CharField(max_length=256,null=True)
    last_login = None

    USERNAME_FIELD = 'username'
    objects=NewUser()

    def __str__(self):
        return self.username

    class Meta:
        db_table="system_user"



class Jump(models.Model):
    name=models.CharField(max_length=256,null=True)
    jumptarget=models.CharField(max_length=256,null=True,blank=True)
    is_jump=models.BooleanField(null=False,default=False)
    relationship=models.ForeignKey(to=settings.AUTH_USER_MODEL,null=True,related_name="jump_target",on_delete=models.CASCADE)
    class Meta:
        db_table="jump"
        ordering=["-id"]





