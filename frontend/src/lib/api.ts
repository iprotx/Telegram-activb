export function createApiHeaders(initData: string): HeadersInit {
  return {
    'Content-Type': 'application/json',
    Authorization: `tma ${initData}`,
  };
}
