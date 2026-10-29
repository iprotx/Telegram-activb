# KEYDROP Mini App

React + TypeScript + Vite frontend for the KEYDROP Telegram Mini App.

The frontend is a presentation/client layer. It must not access PostgreSQL or LittleFox directly; authenticated application data will be obtained through the KEYDROP HTTP API.

## Development

```bash
npm install
npm run dev
```

For Telegram-specific development, initialize the Telegram Mini Apps SDK in the application entrypoint. Local browser development should use the SDK's supported mock environment rather than assuming Telegram globals exist.
