export function createApiHeaders(initData: string): HeadersInit {
  return {
    'Content-Type': 'application/json',
    'X-Telegram-Init-Data': initData,
  };
}
