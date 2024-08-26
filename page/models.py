from django.core.validators import RegexValidator
from django.db import models


class Restaurant(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(verbose_name='Название Ресторана', max_length=50)
    restaurant_email = models.EmailField(verbose_name='Почта ресторана', max_length=60)
    description = models.TextField(verbose_name='Описание')
    address = models.CharField(verbose_name='Адрес Ресторана', max_length=200)
    phone = models.CharField(verbose_name='Номер Ресторана', max_length=12, unique=True)
    TIME_CHOICES = [(f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}') for h in range(24) for m in range(0, 60, 30)]
    reservation_start_time = models.CharField(max_length=50, choices=TIME_CHOICES)
    reservation_end_time = models.CharField(max_length=50, choices=TIME_CHOICES)

    def __str__(self):
        return self.title


class AverageCheck(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Ресторан")
    dish_category = models.CharField(verbose_name="Категории блюд", max_length=100)
    average_cost = models.DecimalField(verbose_name="Средняя стоимость", max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.dish_category} ({self.restaurant.title})"


class WorkingHours(models.Model):
    DAY_OF_WEEK = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]
    TIME_CHOICES = [(f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}') for h in range(24) for m in range(0, 60, 30)]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(verbose_name="День недели", choices=DAY_OF_WEEK)
    open_time = models.CharField(verbose_name="Время открытия", max_length=5, choices=TIME_CHOICES)
    close_time = models.CharField(verbose_name="Время закрытие", max_length=5, choices=TIME_CHOICES)

    def __str__(self):
        return 'Режим работы ' + self.restaurant.title + ' ' + self.get_day_of_week_display()


class Uniqueness(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(verbose_name="Связь с рестораном", max_length=30, null=True, blank=True)
    display_phone = models.BooleanField(default=True)

    address = models.CharField(verbose_name="Адрес", max_length=100, null=True, blank=True)
    display_address = models.BooleanField(default=True)

    district = models.CharField(verbose_name="Район", max_length=50, null=True, blank=True)
    display_district = models.BooleanField(default=True)

    kitchen_type = models.CharField(verbose_name="Кухня", max_length=100, null=True, blank=True)
    display_kitchen_type = models.BooleanField(default=True)

    for_child = models.CharField(verbose_name="Для детей", max_length=100, null=True, blank=True)
    display_for_child = models.BooleanField(default=True)

    deposit = models.CharField(verbose_name="Депозит", max_length=100, null=True, blank=True)
    display_deposit = models.BooleanField(default=True)

    delivery = models.CharField(verbose_name="Доставка", max_length=50, null=True, blank=True)
    display_delivery = models.BooleanField(default=True)

    summer_terrace = models.CharField(verbose_name="Летняя терраса", max_length=50, null=True, blank=True)
    display_summer_terrace = models.BooleanField(default=True)

    vip = models.CharField(verbose_name="VIP", max_length=100, null=True, blank=True)
    display_vip = models.BooleanField(default=True)

    live_music = models.CharField(verbose_name="Живая музыка", max_length=50, null=True, blank=True)
    display_live_music = models.BooleanField(default=True)

    own_pastry_shop = models.CharField(verbose_name="Своя кондитерская", max_length=50, null=True, blank=True)
    display_own_pastry_shop = models.BooleanField(default=True)

    cycle_parking = models.CharField(verbose_name="Велопарковка", max_length=50, null=True, blank=True)
    display_cycle_parking = models.BooleanField(default=True)

    parking = models.CharField(verbose_name="Парковка", max_length=50, null=True, blank=True)
    display_parking = models.BooleanField(default=True)

    breakfast = models.CharField(verbose_name="Завтрак", max_length=100, null=True, blank=True)
    display_breakfast = models.BooleanField(default=True)

    business_lunch = models.CharField(verbose_name="Бизнес-ланч", max_length=100, null=True, blank=True)
    display_business_lunch = models.BooleanField(default=True)

    show_programmes = models.CharField(verbose_name="Шоу программа", max_length=100, null=True, blank=True)
    display_show_programmes = models.BooleanField(default=True)

    Music = models.CharField(verbose_name="Музыка", max_length=50, null=True, blank=True)
    display_Music = models.BooleanField(default=True)

    Chef = models.CharField(verbose_name="Шев-повар", max_length=50, null=True, blank=True)
    display_Chef = models.BooleanField(default=True)

    hallsVenues = models.CharField(verbose_name="Залы и место", max_length=100, null=True, blank=True)
    display_hallsVenues = models.BooleanField(default=True)

    dance_floor = models.CharField(verbose_name="Танцпол", max_length=50, null=True, blank=True)
    display_dance_floor = models.BooleanField(default=True)

    cloakroom = models.CharField(verbose_name="Гардеробная", max_length=50, null=True, blank=True)
    display_cloakroom = models.BooleanField(default=True)

    vegetarian_menu = models.CharField(verbose_name="Вегетарианское меню", max_length=50, null=True, blank=True)
    display_vegetarian_menu = models.BooleanField(default=True)

    own_brewery = models.CharField(verbose_name="Своя Пивоварня", max_length=50, null=True, blank=True)
    display_brewery = models.BooleanField(default=True)

    children_room = models.CharField(verbose_name="Детская комнатка", max_length=50, null=True, blank=True)
    display_children_room = models.BooleanField(default=True)

    cabins = models.CharField(verbose_name="Кабинки", max_length=50, null=True, blank=True)
    display_cabins = models.BooleanField(default=True)

    def __str__(self):
        return 'Особенности ' + self.restaurant.title


class NewsPromotion(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=50)
    subheading = models.CharField(verbose_name="Подзаголовок", max_length=100, blank=True, null=True)
    info = models.TextField(verbose_name="Информация")
    date_created = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    image_url = models.ImageField(verbose_name="Фото", upload_to='news_promotion/')

    def __str__(self):
        return f"{self.name} ({self.restaurant.title})"


class gallery(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image_url = models.ImageField(verbose_name="Фото", upload_to='gallery/')

    def __str__(self):
        return 'Фото Галерея ' + self.restaurant.title


class CategoryMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название Категории", max_length=100)

    def __str__(self):
        return f"{self.name} ({self.restaurant.title})"


class DishMenu(models.Model):
    category = models.ForeignKey(CategoryMenu, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название Блюда", max_length=200)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    ingredients = models.TextField(verbose_name="Состав")
    price = models.DecimalField(verbose_name="Цена", max_digits=6, decimal_places=2)
    image = models.ImageField(verbose_name="Фото", upload_to='Menu/')

    def __str__(self):
        return self.name


class Cart(models.Model):
    guest = models.ForeignKey('rg.Guest', on_delete=models.CASCADE)
    dishes = models.ManyToManyField(DishMenu, through='CartDish')


class CartDish(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish = models.ForeignKey(DishMenu, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(models.Model):
    from rg.models import Guest
    STATUS_CHOOSES = [
        ('0', 'Принят'),
        ('1', 'Готовится'),
        ('2', 'В пути'),
        ('3', 'Доставлен')
    ]
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(DishMenu, through='OrderDish')
    total_cost = models.FloatField(verbose_name="Общая сумма")
    name = models.CharField(verbose_name="Имя", max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+7\d{10}$',
        message="Номер телефона должен быть в формате: '+79999999999'. Всего 11 цифр."
    )
    phone_number = models.CharField(verbose_name="Номер телефона", validators=[phone_regex], max_length=12)
    additional_requests = models.TextField(verbose_name="Особые пожелание", blank=True, null=True)
    address = models.CharField(verbose_name="Адрес", max_length=100)
    status = models.IntegerField(verbose_name="Статус", choices=STATUS_CHOOSES)
    order_time = models.DateTimeField(verbose_name="Время принятие заказа", auto_now_add=True)

    def __str__(self):
        return 'Заказ ' + self.name + ' ' + self.address


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(DishMenu, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class MapData(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    latitude = models.DecimalField(verbose_name="Широта", max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(verbose_name="Долгота", max_digits=9, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return 'Координаты ' + self.restaurant.title


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата")
    TIME_CHOICES = [(f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}') for h in range(24) for m in range(0, 60, 30)]
    time = models.CharField(verbose_name="Время", choices=TIME_CHOICES)
    number_of_people = models.IntegerField(verbose_name="Количество людей")
    name = models.CharField(verbose_name="Имя", max_length=200)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)
    additional_requests = models.TextField(verbose_name="Особые пожелание", blank=True, null=True)

    def __str__(self):
        return f'({self.restaurant.title})' + ' Бронь стола на имя: ' + self.name + ' ' + self.date.strftime('%Y-%m-%d')
