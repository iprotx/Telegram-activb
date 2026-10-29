import { useEffect, useState } from 'react';
import { useLaunchParams } from '@tma.js/sdk-react';

import { fetchProducts, type Product } from './lib/api';
import { getTelegramInitData } from './lib/telegram';

const navigation = ['Главная', 'Каталог', 'Заказы', 'Избранное', 'Профиль'] as const;
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

function formatPrice(product: Product): string {
  return `${(product.price_kopeks / 100).toFixed(2)} ${product.currency}`;
}

export function App() {
  const launchParams = useLaunchParams();
  const platform = launchParams.tgWebAppPlatform;
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [catalogError, setCatalogError] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    void fetchProducts(apiBaseUrl, getTelegramInitData(), controller.signal)
      .then(setProducts)
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') return;
        setCatalogError(true);
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, []);

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
            Каталог управляется сервером KEYDROP. Цены и наличие подтверждаются backend перед
            покупкой.
          </p>
        </section>

        <section className="catalog-section" aria-labelledby="catalog-title">
          <div className="section-heading">
            <div>
              <span className="hero-kicker">Каталог</span>
              <h2 id="catalog-title">Товары</h2>
            </div>
            <span className="section-count">{products.length}</span>
          </div>

          {loading && <p className="state-message">Загружаем каталог…</p>}

          {!loading && catalogError && (
            <p className="state-message error-message">
              Каталог временно недоступен. Попробуйте открыть Mini App ещё раз.
            </p>
          )}

          {!loading && !catalogError && products.length === 0 && (
            <p className="state-message">Пока нет доступных товаров.</p>
          )}

          <div className="product-grid">
            {products.map((product) => (
              <article className="product-card" key={product.id}>
                <div className="product-card-top">
                  <span className="product-category">{product.category ?? 'KEYDROP'}</span>
                  <span className="availability">{product.available ? 'В наличии' : 'Нет'}</span>
                </div>
                <h3>{product.name}</h3>
                {product.description && <p>{product.description}</p>}
                <strong className="product-price">{formatPrice(product)}</strong>
                <button type="button" className="primary-button" disabled={!product.available}>
                  Подробнее
                </button>
              </article>
            ))}
          </div>
        </section>

        <section className="info-grid" aria-label="Статус приложения">
          <article className="info-card">
            <span>Платформа</span>
            <strong>{platform}</strong>
          </article>
          <article className="info-card">
            <span>API</span>
            <strong>{apiBaseUrl}</strong>
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
