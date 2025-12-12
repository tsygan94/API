<template>
  <div class="portfolio-page">
    <div class="container">
      <h2>Наши работы и автомобили в наличии</h2>
      <p class="subtitle">Премиум-класс. Индивидуальный подход. Готовы к выдаче.</p>

      <div v-if="loading" class="loading text-center">
        <div class="spinner"></div>
        <p>Загружаем автомобили...</p>
      </div>

      <div v-else-if="cars.length === 0" class="empty-state">
        <p>Пока нет автомобилей в портфолио</p>
      </div>

      <div v-else class="cars-grid">
        <div v-for="car in cars" :key="car.id" class="car-card">
          <div class="car-image">
            <img 
              :src="car.image || '/no-photo.jpg'" 
              :alt="`${car.brand} ${car.model}`"
              @error="e => e.target.src = '/no-photo.jpg'"
            />
            <div class="price-tag">{{ formatPrice(car.price) }} ₽</div>
            <div v-if="car.is_sold" class="sold-badge">Продано</div>
          </div>
          <div class="car-info">
            <h3>{{ car.brand }} {{ car.model }}</h3>
            <p class="year">{{ car.year }} год</p>
            <router-link :to="`/services?car=${car.id}`" class="btn small">
              Заказать услуги
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const cars = ref([])
const loading = ref(true)

const formatPrice = (price) => {
  return Number(price).toLocaleString('ru-RU')
}

onMounted(async () => {
  try {
    const res = await axios.get('/cars/')  // → http://localhost:8000/api/cars/
    // DRF возвращает либо { results: [...] } либо просто массив
    cars.value = res.data.results || res.data
  } catch (err) {
    console.error('Ошибка загрузки автомобилей:', err)
    cars.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.portfolio-page {
  padding: 4rem 0;
}

.subtitle {
  text-align: center;
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 4rem;
}

.night-mode .subtitle { color: #aaa; }

.cars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 2.5rem;
}

.car-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: all 0.4s;
}

.car-card:hover {
  transform: translateY(-15px) scale(1.02);
  box-shadow: 0 30px 60px rgba(0,0,0,0.22);
}

.night-mode .car-card {
  background: #1e1e1e;
}

.car-image {
  position: relative;
  height: 260px;
  overflow: hidden;
}

.car-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.car-card:hover .car-image img {
  transform: scale(1.08);
}

.price-tag {

  position: absolute;
  top: 15px;
  right: 15px;
  background: #e74c3c;
  color: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.sold-badge {
  position: absolute;
  top: 15px;
  left: 15px;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-weight: 600;
}

.car-info {
  padding: 1.8rem;
  text-align: center;
}

.car-info h3 {
  margin: 0 0 0.5rem;
  font-size: 1.6rem;
  color: #2a5298;
}

.night-mode .car-info h3 { color: #4facfe; }

.year {
  color: #27ae60;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.car-meta {
  color: #777;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.night-mode .car-meta { color: #aaa; }

.btn.small {
  padding: 10px 24px;
  font-size: 0.95rem;
}

.loading, .empty-state {
  text-align: center;
  padding: 6rem 0;
  color: #888;
  font-size: 1.3rem;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 5px solid #f0f0f0;
  border-top: 5px solid #2a5298;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>