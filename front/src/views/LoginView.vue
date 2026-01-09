<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Вход в личный кабинет</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <input 
            v-model="username" 
            type="text" 
            placeholder="Логин" 
            required 
            class="input-field"
          />
        </div>
        <div class="form-group">
          <input 
            v-model="password" 
            type="password" 
            placeholder="Пароль" 
            required 
            class="input-field"
          />
        </div>
        <button type="submit" class="btn full-width">Войти</button>
      </form>
      <p class="auth-link">
        Нет аккаунта? 
        <router-link to="/register">Зарегистрироваться</router-link>
      </p>
      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  error.value = ''
  try {
    const res = await axios.post('/token/', { 
      username: username.value,
      password: password.value
    })
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)
    localStorage.setItem('username', username.value)
    router.push('/profile')
  } catch (err) {
    error.value = 'Неверный логин или пароль'
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
</style>