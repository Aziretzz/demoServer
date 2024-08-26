from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular import openapi
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny

from .serializers import RestaurantCheck
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Restaurant, CategoryMenu, DishMenu, gallery
from .serializers import PostCheckCategory, PutCheckCategory, GetCheckCategory, PostDish, GetDish, PutDish, GetGallery


@csrf_exempt
def page(request):
    return HttpResponse("все работает")


@extend_schema(request=RestaurantCheck, responses={201: RestaurantCheck})
@api_view(['PUT'])
def restaurant_check(request, id):
    try:
        restaurant = Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RestaurantCheck(restaurant, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Создание новой категории",
    request=PostCheckCategory,
    responses={200: PostCheckCategory}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = PostCheckCategory(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': f'Категория "{serializer.data["name"]}" успешно добавлена'},
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@extend_schema(
    description="Удаление категории",
    responses={204: None}
)
def delete_category(request, category_id):
    user = request.user
    restaurant = user.restaurant
    try:
        category_menu = CategoryMenu.objects.get(id=category_id, restaurant=restaurant)
        category_menu.delete()
        return Response(status=204)
    except CategoryMenu.DoesNotExist:
        return Response({"error": "Категория не найдена"}, status=404)


@extend_schema(
    description="Редактирование категории",
    request=PutCheckCategory,
    responses={200: PutCheckCategory(many=True)}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_category(request, category_id):
    user = request.user
    restaurant = user.restaurant
    try:
        category_menu = CategoryMenu.objects.get(id=category_id, restaurant=restaurant)
        serializer = PutCheckCategory(category_menu, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Категория изменена!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CategoryMenu.DoesNotExist:
        return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    description="Получение списка категорий",
    responses={200: GetCheckCategory(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category(request):
    user = request.user
    restaurant = user.restaurant
    categories = CategoryMenu.objects.filter(restaurant=restaurant)
    serializer = GetCheckCategory(categories, many=True)
    return Response(serializer.data)


@extend_schema(
    description="Создание нового блюда",
    request=PostDish,
    responses={201: PostDish}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_dish(request, category_id):
    user = request.user
    restaurant = user.restaurant
    try:
        category_menu = CategoryMenu.objects.get(id=category_id, restaurant=restaurant)
        serializer = PostDish(data=request.data, context={'request': request})
        if serializer.is_valid():
            if 'image' in request.FILES:
                serializer.validated_data['image'] = request.FILES['image']
            dish = serializer.save()
            return Response(PostDish(dish).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CategoryMenu.DoesNotExist:
        return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    description="Удаление блюда",
    responses={204: None}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dish(request, dish_id):
    user = request.user
    restaurant = user.restaurant
    try:
        dish = DishMenu.objects.get(id=dish_id, category__restaurant=restaurant)
        dish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except DishMenu.DoesNotExist:
        return Response({'error': 'Блюдо не найдено'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    description="Получение информации о блюде",
    responses={200: GetDish}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_dish(request, dish_id):
    user = request.user
    restaurant = user.restaurant
    try:
        dish = DishMenu.objects.get(id=dish_id, category__restaurant=restaurant)
        serializer = GetDish(dish)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DishMenu.DoesNotExist:
        return Response({'error': 'Блюдо не найдено'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    description="Получение всех блюд ресторана",
    responses={200: GetDish(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_dishes(request):
    user = request.user
    restaurant = user.restaurant
    dishes = DishMenu.objects.filter(category__restaurant=restaurant)
    serializer = GetDish(dishes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    description="Обновление блюда",
    request=PutDish,
    responses={200: PutDish}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_dish(request, category_id, dish_id):
    user = request.user
    restaurant = user.restaurant
    try:
        category = CategoryMenu.objects.get(id=category_id, restaurant=restaurant)
        dish = DishMenu.objects.get(id=dish_id, category=category)
        serializer = PutDish(dish, data=request.data, context={'request': request})
        if serializer.is_valid():
            if 'image' in request.FILES:
                serializer.validated_data['image'] = request.FILES['image']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CategoryMenu.DoesNotExist:
        return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
    except DishMenu.DoesNotExist:
        return Response({'error': 'Блюдо не найдено'}, status=status.HTTP_404_NOT_FOUND)



@extend_schema(
    description="Получение списка изображений галереи ресторана по ID",
    parameters=[
        OpenApiParameter(
            name='restaurant_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID ресторана',
            required=True
        ),
    ],
    responses={
        200: GetGallery(many=True),
        404: {
            'description': 'Галерея не найдена',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Gallery not found.'
                    }
                }
            }
        },
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery(request, restaurant_id):
    try:
        gallery_images = gallery.objects.filter(restaurant_id=restaurant_id)
        if not gallery_images.exists():
            return Response({"detail": "Gallery not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetGallery(gallery_images, many=True)
        return Response(serializer.data)
    except gallery.DoesNotExist:
        return Response({"detail": "Gallery not found."}, status=status.HTTP_404_NOT_FOUND)