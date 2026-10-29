import ReactDOM from 'react-dom/client';
import { init } from '@tma.js/sdk-react';

import { App } from './App';
import { initializeTelegram } from './lib/telegram';
import './styles.css';

initializeTelegram();
init();

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
