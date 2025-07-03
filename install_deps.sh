#!/bin/bash

echo "🔧 Installing ddddocr MCP Server dependencies..."

# 检查Python版本
python3 --version || {
    echo "❌ Python 3 is required"
    exit 1
}

# 检查Node.js版本
node --version || {
    echo "❌ Node.js is required"
    exit 1
}

# 安装Python依赖
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt || {
    echo "❌ Failed to install Python dependencies"
    exit 1
}

# 安装Node.js依赖
echo "📦 Installing Node.js dependencies..."
npm install || {
    echo "❌ Failed to install Node.js dependencies"
    exit 1
}

echo "✅ All dependencies installed successfully!"
echo "🚀 You can now run: npm run dev" 