<template>
  <div :class="{ 'night-mode': isNight }">
    <header>
      <div class="container header-content">
        <!-- Логотип -->
        <h1>Royal Cars</h1>

        <!-- Десктопная навигация (видна только на больших экранах) -->
        <nav class="desktop-nav">
          <router-link to="/">Главная</router-link>
          <router-link to="/services">Конфигуратор</router-link>
          <router-link to="/portfolio">Портфолио</router-link>
          <router-link to="/about">О нас</router-link>
          <router-link to="/contacts">Контакты</router-link>

          <!-- Если пользователь авторизован -->
          <div v-if="token" class="user-menu">
            <router-link to="/profile">Мои заявки</router-link>
            <button @click="logout" class="logout-btn">Выйти</button>
          </div>
          <!-- Если не авторизован -->
          <div v-else class="auth-links">
            <router-link to="/login">Вход</router-link>
            <router-link to="/register">Регистрация</router-link>
          </div>
        </nav>

        <!-- Кнопка переключения темы -->
        <button class="theme-toggle desktop-only" @click="toggleTheme">
          {{ isNight ? 'Светлая тема' : 'Тёмная тема' }}
        </button>

        <!-- Бургер-меню (только на мобильных) -->
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

      <!-- Затемнение фона при открытом мобильном меню -->
      <div
        class="mobile-menu-overlay"
        :class="{ open: mobileMenuOpen }"
        @click="mobileMenuOpen = false"
      ></div>

      <!-- Боковое мобильное меню -->
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
          <button @click="logout(); mobileMenuOpen = false" class="logout-btn">Выйти</button>
        </div>
        <div v-else class="mobile-auth-links">
          <router-link to="/login" @click="mobileMenuOpen = false">Вход</router-link>
          <router-link to="/register" @click="mobileMenuOpen = false">Регистрация</router-link>
        </div>

        <button class="theme-toggle mobile-theme" @click="toggleTheme">
          {{ isNight ? 'Светлая тема' : 'Тёмная тема' }}
        </button>
      </nav>
    </header>

    <main class="container">
      <router-view />
    </main>

    <footer>
      <div class="container">
        <p>© 2025 Royal Cars. Премиум автомобили и индивидуальный подход.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isNight = ref(localStorage.getItem('theme') === 'night')
const token = ref(localStorage.getItem('access_token'))
const mobileMenuOpen = ref(false)

const toggleTheme = () => {
  isNight.value = !isNight.value
  localStorage.setItem('theme', isNight.value ? 'night' : 'light')
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('username')
  token.value = null
  router.push('/')
}

onMounted(() => {
  if (localStorage.getItem('theme') === 'night') {
    document.body.classList.add('night-mode')
  }
})

watch(isNight, (val) => {
  document.body.classList.toggle('night-mode', val)
})
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

header {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  padding: 1.5rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
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
  padding: 0.6rem 1.4rem !important;
  border-radius: 30px;
  backdrop-filter: blur(10px);
}

.logout-btn {
  background: #e74c3c;
  border: none;
  color: white;
  padding: 0.6rem 1.4rem;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
}

/* Кнопка темы на десктопе */
.theme-toggle {
  background: rgba(255,255,255,0.2);
  color: white;
  border: none;
  padding: 0.7rem 1.4rem;
  border-radius: 30px;
  cursor: pointer;
  font-size: 0.95rem;
  backdrop-filter: blur(10px);
}
.desktop-only { display: block; }

/* Бургер-кнопка */
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

/* Анимация бургера → крестик */
.burger.active span:nth-child(1) { transform: rotate(45deg) translate(8px, 8px); }
.burger.active span:nth-child(2) { opacity: 0; }
.burger.active span:nth-child(3) { transform: rotate(-45deg) translate(8px, -8px); }

/* Затемнение фона */
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

/* Боковое мобильное меню */
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

.mobile-nav.open {
  left: 0;
}

.mobile-nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  color: white;
}

.mobile-nav-header h3 {
  font-size: 1.9rem;
  font-weight: 700;
}

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

.close-btn:hover {
  background: rgba(255,255,255,0.1);
}

.mobile-nav a {
  color: white;
  text-decoration: none;
  font-size: 1.35rem;
  font-weight: 600;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.mobile-nav a:hover {
  color: #a0d8ff;
  padding-left: 0.5rem;
}

.mobile-auth-links a,
.mobile-user-menu a {
  display: block;
  background: rgba(255,255,255,0.15);
  text-align: center;
  padding: 1rem;
  border-radius: 16px;
  margin: 0.8rem 0;
}

.mobile-auth-links a:hover,
.mobile-user-menu a:hover {
  background: rgba(255,255,255,0.25);
}

.mobile-theme {
  margin-top: auto;
  padding: 1rem !important;
  background: rgba(255,255,255,0.15) !important;
  border-radius: 16px;
}

/* Адаптивность */
@media (max-width: 992px) {
  .desktop-nav,
  .desktop-only {
    display: none;
  }
  .burger {
    display: flex;
  }
  .theme-toggle:not(.mobile-theme) {
    display: none;
  }
}

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
}
</style>