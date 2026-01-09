<template>
  <div :class="{ 'night-mode': isNight }">
    <header>
      <div class="container header-content">
        <h1>Royal Cars</h1>

        <nav class="desktop-nav">
          <router-link to="/">Главная</router-link>
          <router-link to="/services">Конфигуратор</router-link>
          <router-link to="/portfolio">Портфолио</router-link>
          <router-link to="/about">О нас</router-link>
          <router-link to="/contacts">Контакты</router-link>

          <div v-if="token" class="user-menu">
            <router-link to="/profile">Мои заявки</router-link>
            <button @click="logout" class="logout-btn">Выйти</button>
          </div>
          <div v-else class="auth-links">
            <router-link to="/login">Вход</router-link>
            <router-link to="/register">Регистрация</router-link>
          </div>
        </nav>

        <button class="theme-toggle desktop-only" @click="toggleTheme">
          {{ isNight ? 'Светлая тема' : 'Тёмная тема' }}
        </button>

        <button
          class="burger"
          :class="{ active: mobileMenuOpen }"
          @click="mobileMenuOpen = !mobileMenuOpen"
          aria-label="Открыть меню"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      <div
        class="mobile-menu-overlay"
        :class="{ open: mobileMenuOpen }"
        @click="mobileMenuOpen = false"
      ></div>

      <nav class="mobile-nav" :class="{ open: mobileMenuOpen }">
        <div class="mobile-nav-header">
          <h3>Royal Cars</h3>
          <button @click="mobileMenuOpen = false" class="close-btn">×</button>
        </div>

        <router-link to="/" @click="mobileMenuOpen = false">Главная</router-link>
        <router-link to="/services" @click="mobileMenuOpen = false">Конфигуратор</router-link>
        <router-link to="/portfolio" @click="mobileMenuOpen = false">Портфолио</router-link>
        <router-link to="/about" @click="mobileMenuOpen = false">О нас</router-link>
        <router-link to="/contacts" @click="mobileMenuOpen = false">Контакты</router-link>

        <div v-if="token" class="mobile-user-menu">
          <router-link to="/profile" @click="mobileMenuOpen = false">Мои заявки</router-link>
          <button @click="logoutAndClose" class="logout-btn">Выйти</button>
        </div>
        <div v-else class="mobile-auth-links">
          <router-link to="/login" @click="mobileMenuOpen = false">Вход</router-link>
          <router-link to="/register" @click="mobileMenuOpen = false">Регистрация</router-link>
        </div>

        <button class="mobile-theme" @click="toggleTheme">
          {{ isNight ? 'Светлая тема' : 'Тёмная тема' }}
        </button>
      </nav>
    </header>

    <main>
      <router-view />
    </main>

    <footer>
      <div class="container">
        <p>&copy; 2025 Royal Cars. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isNight = ref(false)
const mobileMenuOpen = ref(false)

const token = computed(() => localStorage.getItem('access_token'))

const toggleTheme = () => {
  isNight.value = !isNight.value
  if (isNight.value)
  {
    document.body.classList.add('night-mode') 
  } else {
    document.body.classList.remove('night-mode')
  }
  localStorage.setItem('theme', isNight.value ? 'night' : 'light')
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('username')
  router.push('/')
}

const logoutAndClose = () => {
  logout()
  mobileMenuOpen.value = false
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'night' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isNight.value = true
  }
})
</script>

<style scoped>
/* Глобальные переменные и базовые стили */
body {
  margin: 0;
  padding: 0;
  background: #f8f9fa;
  color: #333;
  transition: background 0.3s, color 0.3s;
}

.night-mode body {
  background: #121212;
  color: #e0e0e0;
}

/* Основные контейнеры */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
header {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  padding: 1.5rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.night-mode header {
  background: linear-gradient(135deg, #0f172a, #1e293b);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

h1 {
  color: #fff;
  font-size: 2.4rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin: 0;
}

/* Десктопная навигация */
.desktop-nav {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.desktop-nav a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  transition: all 0.3s;
}

.desktop-nav a:hover,
.desktop-nav a.router-link-active {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.auth-links a,
.user-menu a {
  background: rgba(255,255,255,0.15);
  padding: 0.6rem 1.4rem;
  border-radius: 30px;
  backdrop-filter: blur(10px);
  color: #fff;
  text-decoration: none;
}

.logout-btn {
  background: #e74c3c;
  border: none;
  color: white;
  padding: 0.6rem 1.4rem;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: #c0392b;
}

/* Кнопка темы */
.theme-toggle {
  background: rgba(255,255,255,0.2);
  color: white;
  border: none;
  padding: 0.7rem 1.4rem;
  border-radius: 30px;
  cursor: pointer;
  font-size: 0.95rem;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.theme-toggle:hover {
  background: rgba(255,255,255,0.3);
}

.desktop-only {
  display: block;
}

/* Бургер */
.burger {
  display: none;
  flex-direction: column;
  gap: 6px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.burger span {
  width: 32px;
  height: 3px;
  background: white;
  border-radius: 3px;
  transition: all 0.3s;
}

.burger.active span:nth-child(1) { transform: rotate(45deg) translate(8px, 8px); }
.burger.active span:nth-child(2) { opacity: 0; }
.burger.active span:nth-child(3) { transform: rotate(-45deg) translate(8px, -8px); }

/* Overlay и мобильное меню */
.mobile-menu-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.75);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 9998;
}

.mobile-menu-overlay.open {
  opacity: 1;
  visibility: visible;
}

.mobile-nav {
  position: fixed;
  top: 0;
  left: -340px;
  width: 340px;
  max-width: 85vw;
  height: 100vh;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  padding: 2rem;
  transition: left 0.4s cubic-bezier(0.77, 0, 0.175, 1);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  overflow-y: auto;
}

.night-mode .mobile-nav {
  background: linear-gradient(135deg, #0f172a, #1e293b);
}

.mobile-nav.open { left: 0; }

.mobile-nav-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; color: white; }
.mobile-nav-header h3 { font-size: 1.9rem; font-weight: 700; }

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2.8rem;
  cursor: pointer;
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  transition: background 0.3s;
}

.close-btn:hover { background: rgba(255,255,255,0.1); }

.mobile-nav a {
  color: white;
  text-decoration: none;
  font-size: 1.35rem;
  font-weight: 600;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  transition: all 0.3s;
}

.mobile-nav a:hover { color: #a0d8ff; padding-left: 0.5rem; }

.mobile-auth-links a,
.mobile-user-menu a {
  display: block;
  background: rgba(255,255,255,0.15);
  text-align: center;
  padding: 1rem;
  border-radius: 16px;
  margin: 0.8rem 0;
  color: white;
  text-decoration: none;
  font-weight: 600;
}

.mobile-auth-links a:hover,
.mobile-user-menu a:hover { background: rgba(255,255,255,0.25); }

.mobile-theme {
  margin-top: auto;
  padding: 1rem;
  background: rgba(255,255,255,0.15);
  border-radius: 16px;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  text-align: center;
}

/* Адаптивность */
@media (max-width: 992px) {
  .desktop-nav,
  .desktop-only { display: none; }
  .burger { display: flex; }
  .theme-toggle:not(.mobile-theme) { display: none; }
}

/* Контент и футер */
main {
  min-height: 80vh;
  padding: 4rem 0;
}

footer {
  background: #111;
  color: #aaa;
  text-align: center;
  padding: 3rem 0;
  margin-top: auto;
}

.night-mode footer {
  background: #000;
  color: #ccc;
}

/* Дополнительно: общие ссылки и текст в night-mode */
.night-mode a { color: #a0d8ff; }
.night-mode p, .night-mode li, .night-mode span { color: #e0e0e0; }
.night-mode h2, .night-mode h3 { color: #fff; }
</style>