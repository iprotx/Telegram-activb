import {
  init,
  mockTelegramEnv,
  retrieveRawInitData,
  safeInit,
  themeParams,
  viewport,
} from '@tma.js/sdk';

export async function initializeTelegram(): Promise<void> {
  const result = safeInit();
  if (!result.ok) {
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

  themeParams.mount();
  themeParams.bindCssVars();
  await viewport.safeMount({ timeout: 5000 });
  viewport.bindCssVars();
}

export function getTelegramInitData(): string {
  return retrieveRawInitData() ?? '';
}
