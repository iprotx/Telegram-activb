import { describe, expect, it, vi } from 'vitest';

import { createApiHeaders, fetchProducts } from './api';

describe('createApiHeaders', () => {
  it('sends raw Telegram init data in the authenticated API header', () => {
    const initData = 'user=%7B%22id%22%3A42%7D&auth_date=123&hash=abc';

    expect(createApiHeaders(initData)).toEqual({
      'Content-Type': 'application/json',
      Authorization: `tma ${initData}`,
    });
  });
});

describe('fetchProducts', () => {
  it('returns the server catalog', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          items: [
            {
              id: 1,
              provider_product_id: 42,
              name: 'Test product',
              description: null,
              description_html: null,
              price_kopeks: 19900,
              currency: 'RUB',
              stock: 3,
              stock_unlimited: false,
              available: true,
              category: 'Subscriptions',
            },
          ],
          limit: 50,
        }),
        { status: 200 },
      ),
    );
    vi.stubGlobal('fetch', fetchMock);

    const products = await fetchProducts('https://api.example.test', 'signed-data');

    expect(products[0]?.name).toBe('Test product');
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.example.test/api/v1/products',
      expect.objectContaining({
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'tma signed-data',
        },
      }),
    );
  });

  it('fails with a stable catalog error when the API rejects the request', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('{}', { status: 502 })));

    await expect(fetchProducts('https://api.example.test', 'signed-data')).rejects.toThrow(
      'catalog_unavailable',
    );
  });
});
