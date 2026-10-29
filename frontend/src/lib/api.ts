export interface Product {
  id: number;
  provider_product_id: number;
  name: string;
  description: string | null;
  description_html: string | null;
  price_kopeks: number;
  currency: string;
  stock: number | null;
  stock_unlimited: boolean;
  available: boolean;
  category: string | null;
}

interface ProductsResponse {
  items: Product[];
  limit: number;
}

export function createApiHeaders(initData: string): HeadersInit {
  return {
    'Content-Type': 'application/json',
    Authorization: `tma ${initData}`,
  };
}

export async function fetchProducts(
  baseUrl: string,
  initData: string,
  signal?: AbortSignal,
): Promise<Product[]> {
  const response = await fetch(`${baseUrl}/api/v1/products`, {
    headers: createApiHeaders(initData),
    signal,
  });

  if (!response.ok) {
    throw new Error('catalog_unavailable');
  }

  const payload = (await response.json()) as ProductsResponse;
  return payload.items;
}
