import { reactive } from 'vue';

export interface LogEntry {
  id: number;
  time: string;
  type: 'info' | 'error' | 'warn' | 'data';
  message: string;
  details?: any;
}

export const debugLogs = reactive<LogEntry[]>([]);
let logId = 0;

// 远程日志服务器地址
const REMOTE_LOG_URL = '/api/log';

async function sendToServer(entry: LogEntry) {
  try {
    await fetch(REMOTE_LOG_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entry)
    });
  } catch (e) {
    // 静默失败，避免循环
  }
}

export const logger = {
  info(message: string, details?: any) {
    addLog('info', message, details);
    console.log(`[INFO] ${message}`, details || '');
  },
  error(message: string, details?: any) {
    addLog('error', message, details);
    console.error(`[ERROR] ${message}`, details || '');
  },
  warn(message: string, details?: any) {
    addLog('warn', message, details);
    console.warn(`[WARN] ${message}`, details || '');
  },
  data(message: string, details?: any) {
    addLog('data', message, details);
    console.log(`[DATA] ${message}`, details || '');
  },
  clear() {
    debugLogs.length = 0;
  }
};

function addLog(type: 'info' | 'error' | 'warn' | 'data', message: string, details?: any) {
  const time = new Date().toLocaleTimeString();
  // Clone details to avoid reference issues if object changes later
  let safeDetails = details;
  try {
      if (details) {
          safeDetails = JSON.parse(JSON.stringify(details));
      }
  } catch (e) {
      safeDetails = String(details);
  }

  const entry = { id: logId++, time, type, message, details: safeDetails };
  debugLogs.unshift(entry);
  if (debugLogs.length > 200) debugLogs.pop();
  
  // 发送到服务器
  sendToServer(entry);
}
