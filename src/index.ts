#!/usr/bin/env node

import { spawn, ChildProcess } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import process from 'process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 启动Python MCP服务器
const pythonServerPath = path.join(__dirname, '..', 'ddddocr_mcp_server.py');

async function startServer() {
  try {
    const pythonProcess = spawn('python3', [pythonServerPath], {
      stdio: 'inherit',
      env: { ...process.env },
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to start Python MCP server:', error);
      process.exit(1);
    });

    pythonProcess.on('exit', (code) => {
      console.log(`Python MCP server exited with code ${code}`);
      process.exit(code || 0);
    });

    // 处理进程终止信号
    process.on('SIGINT', () => {
      console.log('Received SIGINT, terminating...');
      pythonProcess.kill('SIGINT');
    });

    process.on('SIGTERM', () => {
      console.log('Received SIGTERM, terminating...');
      pythonProcess.kill('SIGTERM');
    });

  } catch (error) {
    console.error('Error starting server:', error);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  startServer();
} 