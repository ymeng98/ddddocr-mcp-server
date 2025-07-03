# GitHub 设置指南

## 步骤1: 创建GitHub仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 设置仓库信息：
   - **Repository name**: `ddddocr-mcp-server`
   - **Description**: `A powerful MCP server for CAPTCHA recognition using ddddocr`
   - **Visibility**: Public (推荐，这样可以在Smithery上公开分发)
   - **不要**勾选 "Initialize this repository with a README"

## 步骤2: 推送代码到GitHub

在终端中运行以下命令（将YOUR_USERNAME替换为您的GitHub用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/ddddocr-mcp-server.git

# 推送代码
git branch -M main
git push -u origin main
```

## 步骤3: 部署到Smithery

1. 访问 [Smithery.ai](https://smithery.ai/new)
2. 点击 "Deploy a New MCP Server"  
3. 连接您的GitHub账户
4. 选择 `ddddocr-mcp-server` 仓库
5. 确认部署设置
6. 等待部署完成

## 步骤4: 更新package.json

部署前，请更新 `package.json` 中的仓库URL：

```json
{
  "repository": {
    "type": "git",
    "url": "https://github.com/YOUR_USERNAME/ddddocr-mcp-server.git"
  }
}
```

## 验证部署

部署成功后，您的MCP服务器将可以通过以下方式访问：

1. **通过Smithery平台**: 其他用户可以直接搜索并安装您的服务
2. **通过npm**: `npm install ddddocr-mcp-server`
3. **直接从GitHub**: 克隆仓库本地使用

## 注意事项

- 确保仓库是公开的，这样Smithery才能访问
- 第一次部署可能需要几分钟时间
- 可以在Smithery控制台查看部署日志和状态 