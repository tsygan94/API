from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Car(TimeStampedModel):
    brand = models.CharField("Марка", max_length=50)
    model = models.CharField("Модель", max_length=50)
    year = models.PositiveIntegerField("Год")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    is_sold = models.BooleanField("Продано", default=False)
    image = models.ImageField("Фото", upload_to='cars/', null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили в продаже"


class Service(TimeStampedModel):
    name = models.CharField("Услуга", max_length=100)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Стоимость", max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги ремонта"


class Order(TimeStampedModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент", related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автомобиль")
    services = models.ManyToManyField(Service, verbose_name="Услуги")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    total_price = models.DecimalField(
        "Итого",
        max_digits=10,
        decimal_places=2,
        default=0,     
        editable=False
    )
    notes = models.TextField("Примечания", blank=True)
    is_completed = models.BooleanField("Выполнен", default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Пересчитываем сумму после сохранения услуг
        self.total_price = sum(service.price for service in self.services.all())
        super().save(update_fields=['total_price'])

    def __str__(self):
        return f"Заказ #{self.pk} – {self.customer}"

    class Meta:
        verbose_name = "Заказ на ремонт"
        verbose_name_plural = "Заказы на ремонт"


class ContactMessage(TimeStampedModel):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=30, blank=True)
    message = models.TextField("Сообщение")

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"

    class Meta:
        verbose_name = "Сообщение с формы контактов"
        verbose_name_plural = "Сообщения с формы контактов"