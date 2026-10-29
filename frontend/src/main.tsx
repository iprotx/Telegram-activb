import ReactDOM from 'react-dom/client';

import { App } from './App';
import { initializeTelegram } from './lib/telegram';
import './styles.css';

initializeTelegram();

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
