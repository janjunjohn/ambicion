from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, username, email, password, **extra_fields):
    if not username:
      raise ValueError('The given username must be set')
    email = self.normalize_email(email)
    username = self.model.normalize_username(username)
    user = self.model(username=username, email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self.db)
    return user

  def create_user(self, username, email=None, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(username, password, **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True')
    return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField('メールアドレス', max_length=255, unique=True)
  username = models.CharField('ユーザーネーム', max_length=255)
  last_name = models.CharField('苗字', max_length=255)
  first_name = models.CharField('名前', max_length=255)
  password = models.CharField('パスワード', max_length=128)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  class Meta:
    db_table = 'users'
        
    def __str__(self):
      return f'{self.first_name} {self.last_name}'