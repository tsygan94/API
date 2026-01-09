<template>
  <div class="configurator-page container">
    <h2>Оформление заказа в Royal Cars</h2>
    <p class="subtitle">Выберите автомобиль (если покупаете) и нужные услуги</p>

    <div class="config-grid">
      <div class="config-form">
        <div class="select-group">
          <label>Автомобиль (опционально, если покупаете)</label>
          <select v-model="form.car" class="modern-select">
            <option :value="null">— Без покупки автомобиля —</option>
            <option v-for="car in availableCars" :key="car.id" :value="car.id">
              {{ car.brand }} {{ car.model }} {{ car.year }} г. — {{ formatPrice(car.price) }} ₽
            </option>
          </select>
        </div>

        <div class="select-group">
          <label>Выберите услуги</label>
          <div class="services-list">
            <label v-for="service in services" :key="service.id" class="service-checkbox">
              <input type="checkbox" :value="service.id" v-model="form.services" />
              <span>{{ service.name }} — {{ formatPrice(service.price) }} ₽</span>
            </label>
          </div>
        </div>

        <div class="select-group" v-if="notesVisible">
          <label>Примечания к заказу</label>
          <textarea v-model="form.notes" class="modern-textarea" rows="4" placeholder="Дополнительные пожелания..."></textarea>
        </div>

        <div class="price-box">
          <div class="price-label">Итоговая стоимость:</div>
          <div class="price-value">{{ formatPrice(totalPrice) }} ₽</div>
        </div>

        <button v-if="token" @click="createOrder" class="btn full-width large" :disabled="loading">
          {{ loading ? 'Оформляем...' : 'Создать заказ' }}
        </button>
        <router-link v-else to="/login" class="btn full-width large login-btn">
          Войти для оформления
        </router-link>

        <div v-if="orderSuccess" class="success-msg">
          Заказ успешно создан! Скоро свяжемся с вами.
        </div>
        <div v-if="orderError" class="error-msg">
          {{ orderError }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const token = localStorage.getItem('access_token')
const loading = ref(false)
const orderSuccess = ref(false)
const orderError = ref('')

const cars = ref([])
const services = ref([])

const form = ref({
  car: null,
  services: [],
  notes: ''
})

const notesVisible = computed(() => form.value.services.length > 0 || form.value.car !== null)

const availableCars = computed(() => cars.value.filter(car => !car.is_sold))

const totalPrice = computed(() => {
  let total = 0
  if (form.value.car) {
    const car = cars.value.find(c => c.id === form.value.car)
    if (car) total += Number(car.price)
  }
  form.value.services.forEach(id => {
    const service = services.value.find(s => s.id === id)
    if (service) total += Number(service.price)
  })
  return total
})

const formatPrice = (price) => Number(price).toLocaleString('ru-RU')

const loadData = async () => {
  try {
    const [carsRes, servicesRes] = await Promise.all([
      axios.get('/cars/'),
      axios.get('/services/')
    ])
    cars.value = carsRes.data.results || carsRes.data
    services.value = servicesRes.data.results || servicesRes.data
  } catch (err) {
    orderError.value = 'Не удалось загрузить автомобили и услуги'
  }
}

onMounted(loadData)

const createOrder = async () => {
  loading.value = true
  orderError.value = ''
  try {
    await axios.post('/orders/', form.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    orderSuccess.value = true
    form.value = { car: null, services: [], notes: '' }
    await loadData() // Перезагрузка списка машин после покупки
    setTimeout(() => orderSuccess.value = false, 5000)
  } catch (e) {
    orderError.value = e.response?.data?.detail || 'Ошибка создания заказа'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.configurator-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 3rem 0;
}

.config-grid {
  background: white;
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 20px 50px rgba(0,0,0,0.1);
}
.night-mode .config-grid { background: #1e1e1e; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }

.select-group {
  margin-bottom: 2.5rem;
}

.select-group label {
  display: block;
  margin-bottom: 0.8rem;
  font-weight: 600;
  font-size: 1.1rem;
  color: #2a5298;
}
.night-mode .select-group label { color: #4facfe; }

.modern-select,
.modern-textarea,
.input-field {
  width: 100%;
  padding: 16px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 16px;
  font-size: 1.05rem;
  background: #fff;
  transition: all 0.3s;
}
.night-mode .modern-select,
.night-mode .modern-textarea,
.night-mode .input-field {
  background: #2d2d2d;
  border-color: #444;
  color: #fff;
}

.modern-select:focus,
.modern-textarea:focus,
.input-field:focus {
  outline: none;
  border-color: #2a5298;
  box-shadow: 0 0 0 4px rgba(42,82,152,0.15);
}

.services-list {
  max-height: 420px;
  overflow-y: auto;
  padding: 1.5rem;
  background: #f8fbff;
  border-radius: 16px;
  border: 2px solid #eef2f8;
}
.night-mode .services-list {
  background: #252535;
  border-color: #333;
}

.service-checkbox {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  font-size: 1.15rem;
  border-bottom: 1px dashed #ddd;
}
.night-mode .service-checkbox { border-color: #444; }
.service-checkbox:last-child { border-bottom: none; }

.service-checkbox input { transform: scale(1.4); accent-color: #2a5298; }

.price-box {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  color: white;
  padding: 1.8rem;
  border-radius: 20px;
  text-align: center;
  margin: 2.5rem 0;
  font-size: 1.4rem;
}
.price-value {
  font-size: 2.2rem;
  font-weight: 800;
  margin-top: 0.5rem;
}

.login-btn {
  background: #6c757d;
}

.success-msg {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #d4edda;
  color: #155724;
  border-radius: 16px;
  text-align: center;
  font-weight: 600;
}
</style>