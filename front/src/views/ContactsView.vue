<template>
  <div class="contacts-page">
    <div class="container">
      <h2>Контакты</h2>

      <div class="contacts-grid">
        <div class="contact-info">
          <h3>Свяжитесь с нами</h3>
          <div class="info-item">
            <strong>Адрес:</strong>
            <p>Москва, ул. Веницианова, д. 65</p>
          </div>
          <div class="info-item">
            <strong>Телефон:</strong>
            <p>+7 (977) 777-77-99</p>
          </div>
          <div class="info-item">
            <strong>Email:</strong>
            <p>royal_cars@mail.ru</p>
          </div>
          <div class="info-item">
            <strong>Режим работы:</strong>
            <p>Пн–Сб: 10:00–20:00<br>Вс: выходной</p>
          </div>
        </div>

        <div class="contact-form">
          <h3>Обратная связь</h3>
          <form @submit.prevent="sendMessage">
            <input v-model="form.name" placeholder="Ваше имя" required class="input-field" />
            <input v-model="form.email" type="email" placeholder="Email" required class="input-field" />
            <input v-model="form.phone" placeholder="Телефон" class="input-field" />
            <textarea v-model="form.message" placeholder="Ваше сообщение" rows="6" required class="input-field"></textarea>
            <button type="submit" class="btn full-width">Отправить сообщение</button>
          </form>
          <div v-if="sent" class="success-msg">
            Сообщение отправлено! Мы свяжемся с вами в ближайшее время.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  name: '',
  email: '',
  phone: '',
  message: ''
})

const sent = ref(false)
const error = ref('')

const sendMessage = async () => {
  error.value = ''
  
  try {
    await axios.post('/contact/', form.value)   // ← сюда попадёт http://localhost:8000/api/contact/
    
    sent.value = true
    form.value = { name: '', email: '', phone: '', message: '' }

    setTimeout(() => {
      sent.value = false
    }, 6000)
  } catch (err) {
    console.error(err)
    error.value = 'Не удалось отправить сообщение. Попробуйте позже.'
  }
}
</script>

<style scoped>
.contacts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5rem;
  margin-top: 4rem;
}

.contact-info h3,
.contact-form h3 {
  font-size: 1.8rem;
  margin-bottom: 2rem;
  color: #2a5298;
}

.night-mode .contact-info h3,
.night-mode .contact-form h3 { color: #4facfe; }

.info-item {
  margin-bottom: 2rem;
}

.info-item strong {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
}

.night-mode .info-item strong { color: #fff; }

.input-field {
  width: 100%;
  padding: 14px 18px;
  margin-bottom: 1.2rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
}

.input-field:focus {
  outline: none;
  border-color: #2a5298;
}

.night-mode .input-field {
  background: #2d2d2d;
  border-color: #444;
  color: #fff;
}

.success-msg {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #d4edda;
  color: #155724;
  border-radius: 12px;
  text-align: center;
}

@media (max-width: 992px) {
  .contacts-grid {
    grid-template-columns: 1fr;
  }
}
</style>