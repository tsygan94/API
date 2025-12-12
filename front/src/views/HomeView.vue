<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-content">
        <h1>Royal Cars</h1>
        <p class="hero-subtitle">Премиум-автомобили. Индивидуальный подход. Ваш стиль.</p>
        <div class="hero-buttons">
          <router-link to="/services" class="btn large">Конфигуратор</router-link>
          <router-link to="/portfolio" class="btn outline">Наши работы</router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="/cover.webp" alt="Royal Cars">
      </div>
    </section>

    <section class="features">
      <div class="container">
        <h2>Почему выбирают нас</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="icon">Lux</div>
            <h3>Эксклюзивность</h3>
            <p>Только премиум-бренды и индивидуальные решения</p>
          </div>
          <div class="feature-card">
            <div class="icon">Full</div>
            <h3>Полный цикл</h3>
            <p>От конфигурации до обслуживания после покупки</p>
          </div>
          <div class="feature-card">
            <div class="icon">Nice</div>
            <h3>Гарантия качества</h3>
            <p>Официальные дилеры и сертифицированные мастера</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  overflow: hidden;
}

.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  padding: 6rem 0;
  background: linear-gradient(135deg, #f8f9ff 0%, #e8f0fe 100%);
  border-radius: 0 0 100px 100px;
  margin-bottom: 6rem;
}

.night-mode .hero {
  background: linear-gradient(135deg, #121212 0%, #1a1a2e 100%);
}

.hero-content {
  padding-left: 4rem;
}

.hero-content h1 {
  font-size: 4.5rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: #555;
  margin-bottom: 3rem;
}

.night-mode .hero-subtitle { color: #bbb; }

.hero-buttons {
  display: flex;
  gap: 1.5rem;
}

.btn.large {
  padding: 18px 40px !important;
  font-size: 1.2rem;
}

.btn.outline {
  background: transparent;
  border: 2px solid #2a5298;
  color: #2a5298;
  margin-top: auto;
  margin-bottom: auto;
}

.btn.outline:hover {
  background: #2a5298;
  color: white;
}

.hero-image img {
  width: 100%;
  border-radius: 30px;
  box-shadow: 0 30px 60px rgba(0,0,0,0.2);
  transform: perspective(1000px) rotateY(-5deg);
}

.features {
  padding: 6rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3rem;
  margin-top: 4rem;
}

.feature-card {
  text-align: center;
  padding: 2.5rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.08);
  transition: all 0.4s;
}

.feature-card:hover {
  transform: translateY(-15px);
  box-shadow: 0 25px 50px rgba(0,0,0,0.15);
}

.night-mode .feature-card {
  background: #1e1e1e;
}

.icon {
  width: 90px;
  height: 90px;
  margin: 0 auto 1.5rem;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: #2a5298;
}

.night-mode .feature-card h3 { color: #4facfe; }

@media (max-width: 992px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 4rem 0;
  }
  .hero-content { padding: 0 2rem; }
  .hero-image img { transform: none; }
  .features-grid { grid-template-columns: 1fr; }
}
</style>