from rest_framework import serializers
from .models import WorkingHours, Restaurant
from rg.models import Customer
from rg.serializers import registrationCheck
from .models import CategoryMenu, DishMenu


class RestaurantCheck(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['description', 'address', 'phone', 'reservation_start_time', 'reservation_end_time']

    @staticmethod
    def validate_phone_number(value):
        if value.startswith('8'):
            value = '+7' + value[1:]
        if not value.startswith('+7') or len(value) != 12:
            raise serializers.ValidationError('Неправильный номер телефона')
        return value


class PostCheckCategory(serializers.ModelSerializer):
    class Meta:
        model = CategoryMenu
        fields = ['name']

    @staticmethod
    def validate_name(value):
        if CategoryMenu.objects.filter(name=value).exists():
            raise serializers.ValidationError('Категория с таким названием уже существует')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        restaurant = user.restaurant
        validated_data['restaurant'] = restaurant
        return super().create(validated_data)


class PutCheckCategory(serializers.ModelSerializer):
    class Meta:
        model = CategoryMenu
        fields = ['name']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        restaurant = user.restaurant
        validated_data['restaurant'] = restaurant
        return super().update(instance, validated_data)


class GetCheckCategory(serializers.ModelSerializer):
    class Meta:
        model = CategoryMenu
        fields = ['name']


class PostDish(serializers.ModelSerializer):
    class Meta:
        model = DishMenu
        fields = ['name', 'description', 'ingredients', 'price', 'image']

    def validate(self, attrs):
        category_id = self.context['request'].data.get('category')
        user = self.context['request'].user
        restaurant = user.restaurant
        if not CategoryMenu.objects.filter(id=category_id, restaurant=restaurant).exists():
            raise serializers.ValidationError('Категория, которую вы указали, не существует в вашем ресторане!')
        return attrs

    def create(self, validated_data):
        category_id = self.context['request'].data.get('category')
        category = CategoryMenu.objects.get(id=category_id)
        return DishMenu.objects.create(category=category, **validated_data)


class GetDish(serializers.ModelSerializer):
    class Meta:
        model = DishMenu
        fields = ['id', 'category', 'name', 'description', 'ingredients', 'price', 'image']


class PutDish(serializers.ModelSerializer):
    class Meta:
        model = DishMenu
        fields = ['name', 'description', 'ingredients', 'price', 'image']

