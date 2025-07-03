#!/usr/bin/env python3
"""
ddddocr MCP Server 测试脚本
"""

import asyncio
import json
import base64
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from ddddocr_mcp_server import DDDDOCRServer

async def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    server = DDDDOCRServer()
    result = await server._health_check()
    print(f"✅ 健康检查结果: {result[0].text}")
    return True

async def test_ocr_recognition():
    """测试OCR识别"""
    print("🔍 测试OCR识别...")
    
    # 检查测试图片是否存在
    test_image_path = "test_captcha.png"
    if not os.path.exists(test_image_path):
        print(f"❌ 测试图片不存在: {test_image_path}")
        return False
    
    server = DDDDOCRServer()
    
    # 测试使用文件路径
    arguments = {"image_path": test_image_path}
    result = await server._ocr_recognize(arguments)
    print(f"✅ OCR识别结果 (文件路径): {result[0].text}")
    
    # 测试使用base64编码
    with open(test_image_path, 'rb') as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    arguments = {"image_base64": image_base64}
    result = await server._ocr_recognize(arguments)
    print(f"✅ OCR识别结果 (base64): {result[0].text}")
    
    return True

async def test_list_tools():
    """测试工具列表"""
    print("🔍 测试工具列表...")
    server = DDDDOCRServer()
    
    # 模拟MCP工具列表调用
    tools = await server.server._handlers['list_tools']()
    print(f"✅ 可用工具数量: {len(tools)}")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    return True

async def main():
    """主测试函数"""
    print("🚀 开始测试 ddddocr MCP Server")
    print("=" * 50)
    
    tests = [
        ("健康检查", test_health_check),
        ("工具列表", test_list_tools),
        ("OCR识别", test_ocr_recognition),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            success = await test_func()
            if success:
                passed += 1
            print()
        except Exception as e:
            print(f"❌ {test_name}失败: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main()) 