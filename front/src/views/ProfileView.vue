<template>
  <div class="profile-page container">
    <h2>Личный кабинет</h2>

    <div v-if="!token" class="auth-prompt">
      <p>Войдите в аккаунт, чтобы увидеть свои заказы</p>
      <router-link to="/login" class="btn">Войти</router-link>
    </div>

    <div v-else>
      <div class="welcome-msg">
        Добро пожаловать, <strong>{{ username }}</strong>!
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Загружаем ваши заказы...</p>
      </div>

      <div v-else-if="orders.length === 0" class="empty-state">
        <p>У вас пока нет заказов</p>
        <router-link to="/services" class="btn">Перейти в конфигуратор</router-link>
      </div>

      <div v-else class="orders-grid">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <span class="order-id">Заказ №{{ order.id }}</span>
            <span class="order-date">{{ formatDate(order.created_at) }}</span>
            <span class="order-status" :class="{ completed: order.is_completed }">
              {{ order.is_completed ? 'Выполнен' : 'В работе' }}
            </span>
          </div>

          <div class="order-details">
            <p v-if="order.car_info">
              <strong>Автомобиль:</strong>
              {{ order.car_info.brand }} {{ order.car_info.model }} {{ order.car_info.year }} г.
            </p>
            <p v-else><strong>Автомобиль:</strong> — (только услуги)</p>

            <p><strong>Услуги:</strong></p>
            <ul class="services-list">
              <li v-for="service in order.services_info" :key="service.id">
                {{ service.name }} — {{ formatPrice(service.price) }} ₽
              </li>
            </ul>

            <p v-if="order.notes"><strong>Примечания:</strong> {{ order.notes }}</p>

            <div class="order-price">
              <strong>Итого:</strong>
              <span class="price">{{ formatPrice(calculateTotal(order)) }} ₽</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const token = ref(localStorage.getItem('access_token'))
const username = ref(localStorage.getItem('username') || 'Пользователь')
const orders = ref([])
const loading = ref(true)

const formatPrice = (price) => {
  return Number(price).toLocaleString('ru-RU')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

// Подсчёт итоговой суммы для одного заказа (машина + услуги)
const calculateTotal = (order) => {
  let total = 0

  // Цена машины
  if (order.car_info && order.car_info.price) {
    total += Number(order.car_info.price)
  }

  // Цена всех услуг
  if (order.services_info && Array.isArray(order.services_info)) {
    order.services_info.forEach(service => {
      if (service.price) {
        total += Number(service.price)
      }
    })
  }

  return total
}

const loadOrders = async () => {
  if (!token.value) return
  loading.value = true
  try {
    const res = await axios.get('/orders/', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    orders.value = res.data.results || res.data || []
  } catch (err) {
    if (err.response?.status === 401) {
      localStorage.clear()
      router.push('/login')
    }
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadOrders)

watch(token, () => {
  if (token.value) {
    username.value = localStorage.getItem('username') || 'Пользователь'
    loadOrders()
  }
})
</script>

<style scoped>
.profile-page {
  max-width: 1000px;
  margin: 0 auto;
}

.welcome-msg {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 3rem;
  color: #2a5298;
}

.night-mode .welcome-msg { color: #4facfe; }

.empty-state {
  text-align: center;
  padding: 4rem 0;
}

.empty-state p {
  font-size: 1.4rem;
  margin-bottom: 2rem;
  color: #666;
}

.night-mode .empty-state p { color: #aaa; }

.orders-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
}

.order-card {
  background: white;
  border-radius: 20px;
  padding: 1.8rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.order-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.night-mode .order-card {
  background: #1e1e1e;
  box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.night-mode .order-header { border-color: #333; }

.order-id {
  font-weight: 700;
  color: #2a5298;
}

.night-mode .order-id { color: #4facfe; }

.order-date {
  font-size: 0.9rem;
  color: #888;
}

.order-details p {
  margin: 0.8rem 0;
  font-size: 1.05rem;
}

.order-price {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px dashed #eee;
  text-align: right;
}

.night-mode .order-price { border-color: #333; }

.price {
  font-size: 1.6rem;
  color: #27ae60;
  font-weight: 700;
}

@media (max-width: 768px) {
  .orders-grid {
    grid-template-columns: 1fr;
  }
}
</style>