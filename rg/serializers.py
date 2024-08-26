from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Customer, Guest
from django.contrib.auth.hashers import check_password
import re
from page.models import Restaurant


class registrationCheck(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['title', 'email', 'restaurant_email', 'name', 'position', 'phone', 'password']

    @staticmethod
    def validate_email(value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError('Неправильная почта')
        domain = value.split('@')[1]
        if domain not in ["mail.ru", "gmail.com"]:
            raise serializers.ValidationError("Неправильный домен")
        return value

    @staticmethod
    def validate_phone(value):

        if value.startswith('8'):
            value = '+7' + value[1:]
        if not value.startswith('+7'):
            raise serializers.ValidationError('Номер должен начинаться с +7 или 8')
        if len(value) != 12:
            raise serializers.ValidationError('Неправильный номер телефона, он должен содержать 12 символов')

        return value

    @staticmethod
    def validate_password(value):
        if len(value) < 8:
            raise serializers.ValidationError('Пароль должен быть больше 8 символов')
        return value

    def create(self, validated_data):
        restaurant_title = validated_data.pop('title')
        restaurant_email = validated_data.pop('restaurant_email')
        if Restaurant.objects.filter(restaurant_email=restaurant_email).exists():
            raise serializers.ValidationError('Ресторан с таким email уже существует')
        restaurant = Restaurant.objects.create(title=restaurant_title, restaurant_email=restaurant_email)
        validated_data['restaurant'] = restaurant
        validated_data['title'] = restaurant_title
        validated_data['restaurant_email'] = restaurant_email
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


Customer = get_user_model()


class loginCheck(serializers.Serializer):
    title = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        title = data.get('title')
        email = data.get('email')
        password = data.get('password')

        if title and email and password:
            try:
                user = Customer.objects.get(title__iexact=title, email__iexact=email)
            except Customer.DoesNotExist:
                raise serializers.ValidationError('Неправильное название ресторана или адрес электронной почты.')

            if not check_password(password, user.password):
                raise serializers.ValidationError('Неправильный пароль.')
        else:
            raise serializers.ValidationError('Необходимо ввести название ресторана, адрес электронной почты и пароль.')

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class g_registrationCheck(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['email', 'name', 'phone_number', 'password']

    @staticmethod
    def validate_email(value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError('Неправильная почта')
        domain = value.split('@')[1]
        if domain not in ["mail.ru", "gmail.com"]:
            raise serializers.ValidationError("Неправильный домен")
        return value

    @staticmethod
    def validate_phone_number(value):

        if value.startswith('8'):
            value = '+7' + value[1:]
        if not value.startswith('+7'):
            raise serializers.ValidationError('Номер должен начинаться с +7 или 8')
        if len(value) != 12:
            raise serializers.ValidationError('Неправильный номер телефона, он должен содержать 12 символов')

        return value

    @staticmethod
    def validate_password(value):
        if len(value) < 8:
            raise serializers.ValidationError('Пароль должен быть больше 8 символов')
        return value

    def create(self, validated_data):
        user = Guest(
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class g_loginCheck(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = Guest.objects.get(email__iexact=email)
            except Guest.DoesNotExist:
                raise serializers.ValidationError('Неправильный адрес электронной почты.')

            if not check_password(password, user.password):
                raise serializers.ValidationError('Неправильный пароль.')
        else:
            raise serializers.ValidationError('Необходимо ввести адрес электронной почты и пароль.')

        return user
