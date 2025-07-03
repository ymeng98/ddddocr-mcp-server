# ddddocr MCP Server

一个功能强大的MCP（Model Context Protocol）服务器，用于验证码识别，基于ddddocr库构建。

## 功能特性

- 🔤 **文本OCR识别** - 识别验证码中的文字内容
- 🎯 **目标检测** - 检测验证码中的特定目标对象  
- 🔄 **滑块匹配** - 处理滑块验证码，返回准确位置
- ⚡ **高性能** - 基于ONNX运行时，快速响应
- 🔌 **MCP兼容** - 完全兼容Model Context Protocol标准

## 安装使用

### 从Smithery部署（推荐）

1. 访问 [Smithery.ai](https://smithery.ai)
2. 搜索 "ddddocr" 
3. 一键安装到您的AI工具链

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/ddddocr-mcp-server.git
cd ddddocr-mcp-server

# 安装依赖
npm install
pip install -r requirements.txt

# 开发模式运行
npm run dev

# 构建生产版本
npm run build
npm start
```

## 工具说明

### ocr_recognize
识别验证码文本内容

```json
{
  "image_base64": "图片的base64编码",
  "image_path": "图片文件路径"
}
```

### detect_objects  
检测验证码中的目标对象

```json
{
  "image_base64": "图片的base64编码", 
  "image_path": "图片文件路径"
}
```

### match_slider
滑块验证码匹配

```json
{
  "target_base64": "目标图片base64编码",
  "background_base64": "背景图片base64编码",
  "target_path": "目标图片路径",
  "background_path": "背景图片路径"
}
```

### health_check
检查服务健康状态

## 配置使用

将以下配置添加到您的MCP客户端配置文件中：

```json
{
  "servers": {
    "ddddocr": {
      "command": "npx",
      "args": ["ddddocr-mcp-server"]
    }
  }
}
```

## 技术栈

- **核心识别**: ddddocr
- **图像处理**: OpenCV, Pillow
- **数值计算**: NumPy
- **协议**: Model Context Protocol (MCP)
- **运行时**: Python 3.8+, Node.js 18+

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 支持

如有问题，请在GitHub上创建Issue或联系维护者。 