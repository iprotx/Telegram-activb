import { useLaunchParams } from '@tma.js/sdk-react';

const navigation = ['Главная', 'Каталог', 'Заказы', 'Избранное', 'Профиль'] as const;

export function App() {
  const launchParams = useLaunchParams();
  const platform = launchParams.tgWebAppPlatform;

  return (
    <div className="app-shell">
      <header className="top-bar">
        <div>
          <span className="eyebrow">KEYDROP</span>
          <h1>Цифровые товары внутри Telegram</h1>
        </div>
        <span className="status-badge">Mini App</span>
      </header>

      <main className="content">
        <section className="hero-card" aria-labelledby="hero-title">
          <span className="hero-kicker">Добро пожаловать</span>
          <h2 id="hero-title">Покупай быстро. Получай сразу.</h2>
          <p>
            Это фундамент будущего магазина KEYDROP: каталог, заказы, персональные предложения,
            рефералы и коммуникации с нашей собственной клиентской базой.
          </p>
          <button type="button" className="primary-button">
            Открыть каталог
          </button>
        </section>

        <section className="info-grid" aria-label="Статус приложения">
          <article className="info-card">
            <span>Платформа</span>
            <strong>{platform}</strong>
          </article>
          <article className="info-card">
            <span>Статус</span>
            <strong>Frontend foundation</strong>
          </article>
        </section>
      </main>

      <nav className="bottom-navigation" aria-label="Основная навигация">
        {navigation.map((item, index) => (
          <button key={item} type="button" className={index === 0 ? 'nav-item active' : 'nav-item'}>
            {item}
          </button>
        ))}
      </nav>
    </div>
  );
}
