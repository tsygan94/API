from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Car, Service, Order, ContactMessage
from .serializers import CarSerializer, ServiceSerializer, OrderSerializer, UserSerializer, RegisterSerializer, ContactMessageSerializer


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
        # Валидация: нельзя купить проданную машину
        car_id = self.request.data.get('car')
        if car_id:
            try:
                car = Car.objects.get(id=car_id)
                if car.is_sold:
                    raise serializers.ValidationError({"detail": "Этот автомобиль уже продан."})
            except Car.DoesNotExist:
                raise serializers.ValidationError({"detail": "Автомобиль не найден."})

        # Сохраняем — total_price и is_sold посчитаются в model.save()
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('car').prefetch_related('services').all()
        return Order.objects.filter(customer=self.request.user).select_related('car').prefetch_related('services').order_by('-created_at')

class ContactMessageView(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'options']  # Только POST — не нужно GET/DELETE