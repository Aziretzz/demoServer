from . import views
from django.urls import path
from .views import restaurant_check, create_category, delete_category, put_category, get_category
from .views import post_dish, delete_dish, get_one_dish, get_all_dishes, put_dish, get_gallery

urlpatterns = [
    path('', views.page),
    path('restaurant/<int:id>/', restaurant_check, name='restaurant_check'),
    path('category/', create_category, name='create_category'),
    path('category/<int:category_id>/delete/', delete_category, name='delete_category'),
    path('category/<int:category_id>', put_category, name='put_category'),
    path('category', get_category, name='get_category'),
    path('dishes/<int:category_id>', post_dish, name='post_dish'),
    path('dishes/<int:dish_id>/delete/', delete_dish, name='delete_dish'),
    path('dishes/<int:dish_id>/', get_one_dish, name='get_one_dish'),
    path('dishes/', get_all_dishes, name='get_all_dishes'),
    path('dishes/<int:category_id>/<int:dish_id>/', put_dish, name='update_dish'),
    path('gallery/<int:restaurant_id>/', get_gallery, name='get_gallery'),
]
