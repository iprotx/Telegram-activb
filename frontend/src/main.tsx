import ReactDOM from 'react-dom/client';

import { App } from './App';
import { initializeTelegram } from './lib/telegram';
import './styles.css';

async function bootstrap(): Promise<void> {
  await initializeTelegram();
  ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
}

void bootstrap();
