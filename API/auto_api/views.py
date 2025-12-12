from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Car, Service, Order, ContactMessage
from .serializers import CarSerializer, ServiceSerializer, OrderSerializer, UserSerializer, RegisterSerializer, ContactMessageSerializer


# Регистрация (для учебного проекта — без email и т.д.)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('car').prefetch_related('services').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Сначала сохраняем заказ без total_price (он посчитается автоматически в save())
        order = serializer.save(customer=self.request.user)
        
        # Пересчитываем сумму (на случай, если услуг не было)
        order.total_price = sum(service.price for service in order.services.all())
        order.save(update_fields=['total_price'])

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('car').prefetch_related('services').all()
        return Order.objects.filter(customer=self.request.user).select_related('car').prefetch_related('services').order_by('-created_at')


class ContactMessageView(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
