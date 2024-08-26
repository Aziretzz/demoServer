from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Restaurant, AverageCheck, Uniqueness, NewsPromotion, gallery, CategoryMenu, DishMenu, WorkingHours
from .models import MapData, Reservation


class AverageCheckInline(admin.TabularInline):
    model = AverageCheck
    extra = 1
    max_num = 4


class GalleryInline(admin.StackedInline):
    model = gallery
    extra = 1
    max_num = 10


class UniquenessInline(admin.StackedInline):
    model = Uniqueness
    can_delete = False


class NewsPromotionInline(admin.StackedInline):
    model = NewsPromotion
    extra = 1


class WorkingHoursInline(admin.StackedInline):
    model = WorkingHours
    extra = 7
    max_num = 7


class MapDataInline(admin.StackedInline):
    model = MapData


class ReservationInline(admin.StackedInline):
    model = Reservation


# class DishMenuInline(admin.StackedInline):
#     model = DishMenu


class CategoryMenuInline(admin.StackedInline):
    model = CategoryMenu


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [AverageCheckInline, UniquenessInline, NewsPromotionInline, GalleryInline, CategoryMenuInline,
               WorkingHoursInline, MapDataInline,ReservationInline]
    # DishMenuInline
    model = Restaurant
    list_display = ['title', 'address', 'restaurant_email', ]
    search_fields = ('title', 'address', 'restaurant_email', 'phone')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.restaurant.id)

    def has_add_permission(self, request):
        return request.user.is_superuser


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(AverageCheck)
admin.site.register(Uniqueness)
admin.site.register(NewsPromotion)
admin.site.register(gallery)
admin.site.register(CategoryMenu)
admin.site.register(DishMenu)
admin.site.register(WorkingHours)
admin.site.register(MapData)
admin.site.register(Reservation)
