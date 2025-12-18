const http = require('http');
const fs = require('fs');
const path = require('path');

const LOG_FILE = path.join(__dirname, 'frontend.log');
const PORT = 3456;

const server = http.createServer((req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.method === 'POST' && req.url === '/api/log') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const log = JSON.parse(body);
        const line = `[${log.time}] [${log.type.toUpperCase()}] ${log.message} ${log.details ? JSON.stringify(log.details) : ''}\n`;
        fs.appendFileSync(LOG_FILE, line);
        console.log(line.trim());
      } catch (e) {
        console.error('Parse error:', e);
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('{"ok":true}');
    });
  } else if (req.method === 'GET' && req.url === '/api/log') {
    // 读取最近的日志
    try {
      const logs = fs.existsSync(LOG_FILE) ? fs.readFileSync(LOG_FILE, 'utf-8') : '';
      const lines = logs.split('\n').slice(-100).join('\n');
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(lines);
    } catch (e) {
      res.writeHead(500);
      res.end('Error reading logs');
    }
  } else if (req.method === 'GET' && req.url === '/api/log/clear') {
    fs.writeFileSync(LOG_FILE, '');
    res.writeHead(200);
    res.end('Cleared');
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(PORT, () => {
  console.log(`Log server running on http://localhost:${PORT}`);
  console.log(`Logs will be saved to ${LOG_FILE}`);
});
