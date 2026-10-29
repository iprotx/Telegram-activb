import { describe, expect, it } from 'vitest';

import { createApiHeaders } from './api';

describe('createApiHeaders', () => {
  it('sends raw Telegram init data without parsing or mutating it', () => {
    const initData = 'user=%7B%22id%22%3A42%7D&auth_date=123&hash=abc';

    expect(createApiHeaders(initData)).toEqual({
      'Content-Type': 'application/json',
      'X-Telegram-Init-Data': initData,
    });
  });
});
