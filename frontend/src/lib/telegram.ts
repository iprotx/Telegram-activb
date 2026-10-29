import { init, mockTelegramEnv, retrieveRawInitData, safeInit } from '@tma.js/sdk';

export function initializeTelegram(): void {
  const result = safeInit();
  if (result.ok) {
    return;
  }

  mockTelegramEnv({
    launchParams: {
      tgWebAppPlatform: 'tdesktop',
      tgWebAppVersion: '9.0',
      tgWebAppThemeParams: {
        bg_color: '#ffffff',
        text_color: '#111827',
        secondary_bg_color: '#f3f4f6',
        section_bg_color: '#ffffff',
        button_color: '#2aabee',
        button_text_color: '#ffffff',
      },
    },
  });

  init();
}

export function getTelegramInitData(): string {
  return retrieveRawInitData() ?? '';
}
