from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
Customer = get_user_model()


class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ['name', 'email', 'position', ]
    list_filter = ()
    readonly_fields = ('time_create', "time_update", "last_login",)
    fieldsets = (
        ('Basic information', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('title', 'name', 'position', 'phone',)}),
        ('Groups info', {'fields': ('groups',)}),
        ('Permissions', {'fields': (
            'is_admin',
        )}),
        ('time info', {'fields': ('time_create', "time_update", "last_login",)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'title', 'restaurant_email', 'email', 'name', 'position', 'phone', 'password1', 'password2', 'is_admin',
            )}
         ),
    )
    search_fields = ('email', 'title', 'name', 'position', 'phone')
    ordering = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(restaurant=request.user.restaurant)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.restaurant = request.user.restaurant
        super().save_model(request, obj, form, change)


admin.site.register(Customer, CustomerAdmin)


class GroupAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_superuser


# Замените стандартный класс администратора для модели Group на ваш пользовательский класс
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
