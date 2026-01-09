# auto_api/admin.py

from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ExportActionMixin
from .models import Car, Service, Order, ContactMessage


# ========== Ресурсы для экспорта в Excel ==========

class CarResource(resources.ModelResource):
    class Meta:
        model = Car
        fields = ('id', 'brand', 'model', 'year', 'price', 'is_sold', 'created_at', 'updated_at')
        export_order = fields


class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'price', 'created_at', 'updated_at')
        export_order = fields

    
class ContactResource(resources.ModelResource):
    class Meta:
        model = ContactMessage
        fields = ('id', 'name', 'email', 'phone', 'message', 'created_at', 'updated_at')
        export_order = fields


class OrderResource(resources.ModelResource):
    customer = resources.Field(attribute='customer__username', column_name='Клиент')
    car = resources.Field(attribute='car__brand_model_year', column_name='Автомобиль')

    class Meta:
        model = Order
        fields = (
            'id', 'customer', 'car', 'total_price',
            'is_completed', 'created_at', 'notes'
        )
        export_order = fields

    def dehydrate_car(self, obj):
        if obj.car:
            return f"{obj.car.brand} {obj.car.model} ({obj.car.year})"
        return "—"


# ========== Инлайны ==========

class OrderServiceInline(admin.TabularInline):
    model = Order.services.through
    extra = 1
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги в заказе"


# ========== Админки ==========

@admin.register(Car)
class CarAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = CarResource
    
    list_display = ['brand', 'model', 'year', 'price', 'is_sold', 'image_preview']
    list_filter = ['brand', 'year', 'is_sold', 'created_at']
    search_fields = ['brand', 'model']
    list_editable = ['price', 'is_sold']
    readonly_fields = ['image_preview_full']

    fieldsets = (
        (None, {
            'fields': ('brand', 'model', 'year', 'price', 'is_sold')
        }),
        ('Картинка', {
            'fields': ('image_url', 'image_preview_full'),
            'description': 'Вставьте прямую ссылку на изображение (например, с unsplash.com или imgur.com)'
        }),
    )

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="height: 70px; border-radius: 6px;">', obj.image_url)
        return "—"
    image_preview.short_description = "Превью"

    def image_preview_full(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-width: 600px; border-radius: 8px;">', obj.image_url)
        return "Нет ссылки"
    image_preview_full.short_description = "Полное фото"


@admin.register(Service)
class ServiceAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ServiceResource
    
    list_display = ['name', 'price', 'created_at']
    search_fields = ['name']
    list_editable = ['price']
    ordering = ['price']


@admin.register(Order)
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = OrderResource
    
    list_display = ['id', 'customer', 'car_display', 'total_price', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at', 'services']
    search_fields = ['customer__username', 'car__brand', 'car__model']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [OrderServiceInline]

    fieldsets = (
        (None, {
            'fields': ('customer', 'car', 'is_completed', 'notes')
        }),
        ('Автоматически', {
            'fields': ('total_price', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def car_display(self, obj):
        if obj.car:
            return f"{obj.car.brand} {obj.car.model} ({obj.car.year})"
        return "— (только услуги)"
    car_display.short_description = "Автомобиль"


@admin.register(ContactMessage)
class ContactMessageAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'email']
    ordering = ['-created_at']