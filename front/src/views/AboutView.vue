<template>
  <div class="about-page">
    <div class="container">
      <h2>О компании Royal Cars</h2>
      <div class="about-content">
        <div class="about-text">
          <p class="lead">
            Royal Cars — это не просто автосалон. Это место, где рождаются мечты о совершенном автомобиле.
          </p>
          <p>
            Мы специализируемся на премиум-сегменте: BMW, Mercedes-Benz, Audi, Porsche. 
            Наша миссия — дать вам возможность создать автомобиль, который будет отражать ваш статус, вкус и характер.
          </p>
          <p>
            От индивидуальной конфигурации до полного цикла обслуживания — мы рядом на каждом этапе.
          </p>
        </div>
      </div>

      <div class="team-section">
        <h2>Наша команда</h2>
        <div class="team-grid">
          <div class="team-member">
            <img src="/director.jpg" alt="Александр Петров">
            <h3>Александр Петров</h3>
            <p>Генеральный директор</p>
          </div>
          <div class="team-member">
            <img src="/meh.webp" alt="Елена Смирнова">
            <h3>Елена Смирнова</h3>
            <p>Главный технолог</p>
          </div>
          <div class="team-member">
            <img src="/menedger.jpg" alt="Дмитрий Иванов">
            <h3>Дмитрий Иванов</h3>
            <p>Менеджер по продажам</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-content {
  margin: 5rem 0;
}

.lead {
  font-size: 1.4rem;
  line-height: 1.8;
  color: #2a5298;
  margin-bottom: 1.5rem;
}

.night-mode .lead { color: #4facfe; }

.about-image img {
  width: 100%;
  border-radius: 30px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.2);
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-top: 4rem;
}

.team-member {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.team-member img {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 1.5rem;
  border: 5px solid #f0f0f0;
}

.team-member h3 {
  margin-bottom: 0.5rem;
  color: #2a5298;
}

.night-mode .team-member {
  background: #1e1e1e;
}

@media (max-width: 768px) {
  .about-content {
    grid-template-columns: 1fr;
  }
}
</style>