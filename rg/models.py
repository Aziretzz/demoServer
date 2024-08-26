from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from page.models import Restaurant


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, name, position, phone):
        if not email:
            raise ValueError("Пользователь должен иметь адрес электронной почты")
        if not password:
            raise ValueError("Пользователь должен иметь пароль")
        if not phone:
            raise ValueError("Пользователь должен иметь номер телефона")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            position=position,
            phone=phone)
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, phone):
        if not email:
            raise ValueError("Пользователь должен иметь адрес электронной почты")
        if not password:
            raise ValueError("Пользователь должен иметь пароль")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            name=name,
            phone=phone,
        )
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    last_login = models.DateTimeField(verbose_name='Время входа в аккаунт', auto_now=True)
    time_create = models.DateTimeField(verbose_name='Время создания аккаунта', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время последнего изменения', auto_now=True)
    title = models.CharField(verbose_name='Название Ресторана', max_length=200)
    email = models.EmailField(verbose_name='Почта пользователя', max_length=60, unique=True)
    restaurant_email = models.EmailField(verbose_name='Почта ресторана', max_length=60)
    name = models.CharField(verbose_name='ФИО', max_length=100)
    position = models.CharField(verbose_name='Должность', max_length=30)
    phone = models.CharField(verbose_name='Номер телефона', max_length=12, unique=True)
    is_admin = models.BooleanField(verbose_name='Админ', default=True)
    is_superuser = models.BooleanField(verbose_name='Всемогущий', default=False)
    restaurant = models.ForeignKey(Restaurant, related_name='restaurants', on_delete=models.CASCADE)

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser

    @property
    def is_staff(self):
        return self.is_admin or self.is_superuser

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.title

    def __str__(self):
        return self.email


class JWTToken(models.Model):
    user = models.OneToOneField(
        'Customer',
        related_name='jwt_token',
        on_delete=models.CASCADE,
    )
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    access_expires_at = models.DateTimeField()
    refresh_expires_at = models.DateTimeField()

    class Meta:
        db_table = 'jwt_token'


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, password):
        if not email:
            raise ValueError('Пользователи должны иметь адрес электронной почты')
        if not phone_number:
            raise ValueError('Пользователи должны иметь номер телефона')
        if not password:
            raise ValueError("Пользователь должен иметь пароль")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)

        return user


class Guest(AbstractBaseUser):
    last_login = models.DateTimeField(verbose_name='Время входа в аккаунт', auto_now=True)
    time_create = models.DateTimeField(verbose_name='Время создания аккаунта', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время последнего изменения', auto_now=True)
    email = models.EmailField(verbose_name='Адрес электронной почты', max_length=255, unique=True)
    name = models.CharField(verbose_name='ФИО', max_length=255)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=12, unique=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    class Meta:
        db_table = 'guest'

    def __str__(self):
        return self.email + ' ' + self.name


class GJWTToken(models.Model):
    user = models.OneToOneField(
        'Guest',
        related_name='g_jwt_token',
        on_delete=models.CASCADE,
    )
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    access_expires_at = models.DateTimeField()
    refresh_expires_at = models.DateTimeField()

    class Meta:
        db_table = 'g_jwt_token'
