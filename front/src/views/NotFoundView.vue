<template>
  <div class="not-found-page">
    <div class="container">
      <div class="error-content">
        <h1 class="error-code">404</h1>
        <h2>Страница не найдена</h2>
        <p class="error-text">
          К сожалению, запрошенная страница не существует.<br>
          Возможно, она была удалена или вы ввели неправильный адрес.
        </p>

        <div class="error-actions">
          <router-link to="/" class="btn large">
            Вернуться на главную
          </router-link>
          <button @click="goBack" class="btn outline large">
            Назад
          </button>
        </div>

        <div class="error-car">
          <p v-if="!hasImage" class="fallback-text">🚗</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const goBack = () => {
  router.go(-1)
}

const hasImage = true // просто для fallback, если картинки нет
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9ff 0%, #e8f0fe 100%);
  padding: 2rem 0;
}

.night-mode .not-found-page {
  background: linear-gradient(135deg, #121212 0%, #1a1a2e 100%);
}

.error-content {
  text-align: center;
  max-width: 700px;
  padding: 3rem;
  background: white;
  border-radius: 30px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.15);
  position: relative;
  overflow: hidden;
}

.night-mode .error-content {
  background: #1e1e1e;
  box-shadow: 0 30px 80px rgba(0,0,0,0.6);
}

.error-code {
  font-size: 12rem;
  font-weight: 900;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.night-mode .error-code {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

h2 {
  font-size: 2.8rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.night-mode h2 {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.error-text {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 3rem;
  line-height: 1.8;
}

.night-mode .error-text {
  color: #aaa;
}

.error-actions {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.btn.large {
  padding: 18px 40px;
  font-size: 1.2rem;
}

.btn.outline {
  background: transparent;
  border: 2px solid #2a5298;
  color: #2a5298;
}

.btn.outline:hover {
  background: #2a5298;
  color: white;
}

.error-car {
  margin-top: 2rem;
}

.error-car img {
  max-width: 100%;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.fallback-text {
  font-size: 8rem;
  opacity: 0.3;
}

/* Адаптивность */
@media (max-width: 768px) {
  .error-code {
    font-size: 8rem;
  }
  h2 {
    font-size: 2.2rem;
  }
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  .btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>