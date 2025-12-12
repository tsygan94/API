# auto_api/tests.py

import os
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Car, Service, Order, ContactMessage


class AutoAPITests(APITestCase):
    def setUp(self):
        # Очищаем всё перед каждым тестом — гарантируем чистую БД
        User.objects.all().delete()
        Car.objects.all().delete()
        Service.objects.all().delete()
        Order.objects.all().delete()
        ContactMessage.objects.all().delete()

        self.client = APIClient()

        # Пользователи
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')

        # Данные
        self.car = Car.objects.create(
            brand="Toyota",
            model="Camry",
            year=2022,
            price=Decimal('3500000.00'),
            is_sold=False,
        )

        self.service1 = Service.objects.create(
            name="Замена масла",
            price=Decimal('3500.00')
        )
        self.service2 = Service.objects.create(
            name="Шиномонтаж",
            price=Decimal('2000.00')
        )

    # ========================
    #   Регистрация и токен
    # ========================

    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_obtain_jwt_token(self):
        url = '/api/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        return response.data['access']

    # ========================
    #   Cars – публичные (AllowAny)
    # ========================

    def test_get_cars_list(self):
        response = self.client.get(reverse('car-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ровно один объект создан в setUp
        self.assertEqual(len(response.data['results'] if 'results' in response.data else response.data), 1)

    def test_regular_user_can_create_car(self):
        """У тебя стоит AllowAny — значит обычный юзер может создавать"""
        self.client.force_authenticate(user=self.user)
        data = {
            "brand": "Lada",
            "model": "Vesta",
            "year": 2024,
            "price": "1200000.00",
        }
        response = self.client.post(reverse('car-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)

    # ========================
    #   Services – тоже публичные
    # ========================

    def test_get_services_list(self):
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ровно два сервиса создано в setUp
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 2)

    # ========================
    #   Orders – только аутентифицированные + фильтрация по пользователю
    # ========================

    def test_create_order_with_services(self):
        token = self.test_obtain_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        data = {
            "car": self.car.id,
            "services": [self.service1.id, self.service2.id],
            "notes": "Срочно!"
        }
        response = self.client.post(reverse('order-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['total_price']), Decimal('5500.00'))

        order = Order.objects.get(pk=response.data['id'])
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.services.count(), 2)

    def test_user_sees_only_own_orders(self):
        # Создаём заказы явно в этом тесте
        Order.objects.create(customer=self.user, car=self.car, total_price=1000).services.set([self.service1])
        other_user = User.objects.create_user(username='other', password='pass')
        Order.objects.create(customer=other_user, total_price=9999)

        token = self.test_obtain_jwt_token()  # от testuser
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 1)  # только свой заказ

    def test_admin_sees_all_orders(self):
        Order.objects.create(customer=self.user, total_price=5000)
        other = User.objects.create_user(username='u2', password='p')
        Order.objects.create(customer=other, total_price=7000)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('order-list'))
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertGreaterEqual(len(data), 2)

    def test_unauthenticated_cannot_create_order(self):
        data = {"services": [self.service1.id]}
        response = self.client.post(reverse('order-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ========================
    #   Contact Message
    # ========================

    def test_create_contact_message(self):
        data = {
            "name": "Иван",
            "email": "ivan@test.ru",
            "phone": "+7999",
            "message": "Хочу записаться"
        }
        response = self.client.post(reverse('contactmessage-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ContactMessage.objects.filter(email="ivan@test.ru").exists())

    # ========================
    #   Документация
    # ========================

    def test_swagger_accessible(self):
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_accessible(self):
        response = self.client.get('/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)