FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖，包括OpenCV所需的libGL
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 首先安装Node.js（用于MCP包装器）
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 复制Python依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制Node.js配置文件
COPY package*.json tsconfig.json ./

# 安装Node.js依赖
RUN npm install

# 复制应用代码
COPY . .

# 构建TypeScript
RUN npm run build

# 暴露端口（如果需要HTTP接口）
EXPOSE 3000

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

# 启动MCP服务器
CMD ["python3", "ddddocr_mcp_server.py"] 