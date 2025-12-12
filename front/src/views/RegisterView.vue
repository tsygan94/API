<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Регистрация</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <input v-model="username" type="text" placeholder="Придумайте логин" required class="input-field" />
        </div>
        <div class="form-group">
          <input v-model="password" type="password" placeholder="Придумайте пароль" required class="input-field" />
        </div>
        <div class="form-group">
          <input v-model="password2" type="password" placeholder="Повторите пароль" required class="input-field" />
        </div>
        <button type="submit" class="btn full-width">Зарегистрироваться</button>
      </form>
      <p class="auth-link">
        Уже есть аккаунт? 
        <router-link to="/login">Войти</router-link>
      </p>
      <div v-if="error" class="error-msg">{{ error }}</div>
      <div v-if="success" class="success-msg">{{ success }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')
const success = ref('')
const router = useRouter()

const register = async () => {
  if (password.value !== password2.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  try {
    await axios.post('/register/', {
      username: username.value,
      password: password.value
    })
    success.value = 'Регистрация успешна! Теперь войдите в систему.'
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    error.value = 'Ошибка регистрации. Возможно, логин занят.'
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-card {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.night-mode .auth-card {
  background: #1e1e1e;
  box-shadow: 0 15px 35px rgba(0,0,0,0.4);
}

.form-group {
  margin-bottom: 1.5rem;
}

.input-field {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s;
}

.input-field:focus {
  outline: none;
  border-color: #2a5298;
  box-shadow: 0 0 0 4px rgba(42, 82, 152, 0.2);
}

.night-mode .input-field {
  background: #2d2d2d;
  border-color: #444;
  color: #fff;
}

.full-width {
  width: 100%;
  margin-top: 1rem;
}

.auth-link {
  margin-top: 1.5rem;
  color: #666;
}

.auth-link a {
  color: #2a5298;
  font-weight: 600;
}

.error-msg {
  margin-top: 1rem;
  color: #e74c3c;
  font-weight: 500;
}

.success-msg {
  margin-top: 1rem;
  color: #27ae60;
  font-weight: 500;
}

/* Если у тебя где-то определён .btn — добавь на всякий случай */
.btn {
  padding: 14px 20px;
  background: #2a5298;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #1e40af;
}

.night-mode .btn {
  background: #3b82f6;
}

.night-mode .btn:hover {
  background: #2563eb;
}
</style>