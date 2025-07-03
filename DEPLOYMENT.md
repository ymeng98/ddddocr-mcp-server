# 部署指南

## Smithery.ai 部署

### 前提条件
确保您的GitHub仓库包含以下文件：
- ✅ `Dockerfile` - Docker构建配置
- ✅ `smithery.yaml` - Smithery平台配置
- ✅ `requirements.txt` - Python依赖
- ✅ `package.json` - Node.js包配置

### 部署步骤

1. **访问Smithery部署页面**
   ```
   https://smithery.ai/new
   ```

2. **连接GitHub账户**
   - 点击 "Connect GitHub"
   - 授权Smithery访问您的仓库

3. **选择仓库**
   - 选择 `ymeng98/ddddocr-mcp-server`
   - Smithery会自动检测 `smithery.yaml` 配置

4. **确认配置**
   - 检查资源配置：1GB内存，0.5CPU
   - 确认环境变量设置
   - 验证Docker构建配置

5. **开始部署**
   - 点击 "Deploy"
   - 等待构建完成（通常5-10分钟）

### 构建过程说明

#### Docker构建阶段
1. **基础镜像**: Python 3.11-slim
2. **系统依赖**: 安装OpenCV所需的libGL等库
3. **Node.js**: 安装Node.js 18.x用于MCP包装
4. **Python依赖**: 安装ddddocr、opencv-python等
5. **应用代码**: 复制和构建项目文件

#### 关键解决方案
- ✅ **libGL问题**: 通过安装 `libgl1-mesa-glx` 解决OpenCV依赖
- ✅ **内存优化**: 1GB内存足够运行ddddocr模型
- ✅ **MCP协议**: 直接启动Python MCP服务器

### 部署后验证

部署成功后，您可以通过以下方式验证：

1. **健康检查**
   ```json
   {
     "tool": "health_check",
     "arguments": {}
   }
   ```

2. **OCR测试**
   ```json
   {
     "tool": "ocr_recognize", 
     "arguments": {
       "image_base64": "your_base64_image_data"
     }
   }
   ```

### 故障排除

#### 常见问题

**问题1**: OpenCV libGL错误
```
ImportError: libGL.so.1: cannot open shared object file
```
**解决方案**: 已在Dockerfile中添加 `libgl1-mesa-glx` 依赖

**问题2**: 内存不足
```
Killed (signal 9)
```
**解决方案**: 在smithery.yaml中设置了1GB内存限制

**问题3**: MCP协议连接失败
```
Failed to connect to MCP server
```
**解决方案**: 确保使用stdio协议，直接启动Python服务器

### 本地测试

如果需要本地测试Docker镜像：

```bash
# 构建镜像
docker build -t ddddocr-mcp-server .

# 运行容器
docker run -p 3000:3000 ddddocr-mcp-server

# 测试MCP连接
python3 test_mcp_server.py
```

### 更新部署

要更新已部署的服务：

1. 推送新代码到GitHub
2. 在Smithery控制台点击 "Redeploy"
3. 等待新版本构建完成
4. 验证更新是否成功

### 监控和日志

- **部署状态**: Smithery控制台实时显示
- **构建日志**: 查看详细的Docker构建过程
- **运行日志**: 监控MCP服务器运行状态
- **健康检查**: 自动检测服务可用性

### 资源配置

当前配置适合大多数使用场景：
- **内存**: 1GB（足够加载ddddocr模型）
- **CPU**: 0.5核（平衡性能和成本）
- **存储**: 临时文件存储
- **网络**: 标准MCP协议通信 