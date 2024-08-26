from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Restaurant, CategoryMenu


@receiver(post_save, sender=Restaurant)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        categories = ['Горячие блюда', 'Десерты', 'Салаты', 'Завтраки', 'Холодные напитки']
        for category_name in categories:
            CategoryMenu.objects.create(name=category_name, restaurant=instance)
