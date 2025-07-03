FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖，包括OpenCV所需的库
RUN apt-get update && apt-get install -y \
    curl \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    libfontconfig1 \
    libxss1 \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 首先复制并安装Python依赖（利用Docker缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制Node.js配置文件
COPY package.json ./
# 只安装生产依赖，跳过TypeScript构建
RUN npm install --only=production || npm install

# 复制应用代码
COPY ddddocr_mcp_server.py .
COPY test_captcha.png .

# 创建一个简单的健康检查脚本
RUN echo '#!/bin/bash\npython3 -c "import ddddocr; print(\"OK\")"' > /app/health_check.sh \
    && chmod +x /app/health_check.sh

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 暴露端口（标准MCP通信不需要HTTP端口）
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /app/health_check.sh || exit 1

# 启动MCP服务器
CMD ["python3", "ddddocr_mcp_server.py"] 