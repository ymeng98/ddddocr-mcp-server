#!/usr/bin/env python3
"""
ddddocr MCP Server
提供验证码识别服务的MCP服务器
"""

import asyncio
import json
import base64
from io import BytesIO
from typing import Any, Optional, Dict, List
import logging

# MCP imports
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# ddddocr imports
import ddddocr
import cv2
import numpy as np
from PIL import Image

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ddddocr-mcp")

class DDDDOCRServer:
    def __init__(self):
        self.server = Server("ddddocr-mcp")
        self.ocr = None
        self.det = None
        self.slide = None
        self._setup_handlers()
        
    def _setup_handlers(self):
        """设置MCP处理器"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """列出可用工具"""
            return [
                Tool(
                    name="ocr_recognize",
                    description="识别验证码文本内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_base64": {
                                "type": "string",
                                "description": "base64编码的图片数据"
                            },
                            "image_path": {
                                "type": "string", 
                                "description": "图片文件路径"
                            }
                        },
                        "anyOf": [
                            {"required": ["image_base64"]},
                            {"required": ["image_path"]}
                        ]
                    }
                ),
                Tool(
                    name="detect_objects",
                    description="检测验证码中的目标对象",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_base64": {
                                "type": "string",
                                "description": "base64编码的图片数据"
                            },
                            "image_path": {
                                "type": "string",
                                "description": "图片文件路径"
                            }
                        },
                        "anyOf": [
                            {"required": ["image_base64"]},
                            {"required": ["image_path"]}
                        ]
                    }
                ),
                Tool(
                    name="match_slider",
                    description="滑块验证码匹配，返回滑块位置",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target_base64": {
                                "type": "string",
                                "description": "目标图片base64编码"
                            },
                            "background_base64": {
                                "type": "string", 
                                "description": "背景图片base64编码"
                            },
                            "target_path": {
                                "type": "string",
                                "description": "目标图片文件路径"
                            },
                            "background_path": {
                                "type": "string",
                                "description": "背景图片文件路径"
                            }
                        },
                        "anyOf": [
                            {"required": ["target_base64", "background_base64"]},
                            {"required": ["target_path", "background_path"]}
                        ]
                    }
                ),
                Tool(
                    name="health_check",
                    description="检查ddddocr服务健康状态",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """处理工具调用"""
            try:
                if name == "health_check":
                    return await self._health_check()
                elif name == "ocr_recognize":
                    return await self._ocr_recognize(arguments)
                elif name == "detect_objects":
                    return await self._detect_objects(arguments)
                elif name == "match_slider":
                    return await self._match_slider(arguments)
                else:
                    return [TextContent(
                        type="text",
                        text=f"未知工具: {name}"
                    )]
            except Exception as e:
                logger.error(f"工具调用错误 {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"错误: {str(e)}"
                )]

    def _init_ocr(self):
        """初始化OCR模块"""
        if self.ocr is None:
            try:
                self.ocr = ddddocr.DdddOcr()
                logger.info("OCR模块初始化成功")
            except Exception as e:
                logger.error(f"OCR模块初始化失败: {e}")
                raise

    def _init_det(self):
        """初始化目标检测模块"""
        if self.det is None:
            try:
                self.det = ddddocr.DdddOcr(det=True)
                logger.info("目标检测模块初始化成功")
            except Exception as e:
                logger.error(f"目标检测模块初始化失败: {e}")
                raise

    def _init_slide(self):
        """初始化滑块模块"""
        if self.slide is None:
            try:
                self.slide = ddddocr.DdddOcr(det=False, ocr=False)
                logger.info("滑块模块初始化成功")
            except Exception as e:
                logger.error(f"滑块模块初始化失败: {e}")
                raise

    def _load_image(self, image_base64: Optional[str] = None, image_path: Optional[str] = None) -> bytes:
        """加载图片数据"""
        if image_base64:
            return base64.b64decode(image_base64)
        elif image_path:
            with open(image_path, 'rb') as f:
                return f.read()
        else:
            raise ValueError("必须提供image_base64或image_path")

    async def _health_check(self) -> List[TextContent]:
        """健康检查"""
        try:
            status = {
                "service": "ddddocr-mcp",
                "status": "healthy",
                "modules": {
                    "ocr": self.ocr is not None,
                    "detection": self.det is not None, 
                    "slider": self.slide is not None
                },
                "version": "1.0.0"
            }
            return [TextContent(
                type="text",
                text=json.dumps(status, indent=2, ensure_ascii=False)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"健康检查失败: {str(e)}"
            )]

    async def _ocr_recognize(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """OCR识别"""
        try:
            self._init_ocr()
            
            image_data = self._load_image(
                arguments.get("image_base64"),
                arguments.get("image_path")
            )
            
            result = self.ocr.classification(image_data)
            
            response = {
                "success": True,
                "result": result,
                "type": "ocr_recognition"
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(response, ensure_ascii=False)
            )]
            
        except Exception as e:
            logger.error(f"OCR识别错误: {e}")
            response = {
                "success": False,
                "error": str(e),
                "type": "ocr_recognition"
            }
            return [TextContent(
                type="text",
                text=json.dumps(response, ensure_ascii=False)
            )]

    async def _detect_objects(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """目标检测"""
        try:
            self._init_det()
            
            image_data = self._load_image(
                arguments.get("image_base64"),
                arguments.get("image_path")
            )
            
            poses = self.det.detection(image_data)
            
            response = {
                "success": True,
                "result": poses,
                "count": len(poses),
                "type": "object_detection"
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(response, ensure_ascii=False)
            )]
            
        except Exception as e:
            logger.error(f"目标检测错误: {e}")
            response = {
                "success": False,
                "error": str(e),
                "type": "object_detection"
            }
            return [TextContent(
                type="text",
                text=json.dumps(response, ensure_ascii=False)
            )]

    async def _match_slider(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """滑块匹配"""
        try:
            self._init_slide()
            
            # 加载目标图片和背景图片
            target_data = self._load_image(
                arguments.get("target_base64"),
                arguments.get("target_path")
            )
            
            background_data = self._load_image(
                arguments.get("background_base64"),
                arguments.get("background_path")
            )
            
            result = self.slide.slide_match(target_data, background_data)
            
            response = {
                "success": True,
                "result": result,
                "type": "slider_match"
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(response, ensure_ascii=False)
            )]
            
        except Exception as e:
            logger.error(f"滑块匹配错误: {e}")
            response = {
                "success": False,
                "error": str(e),
                "type": "slider_match"
            }
            return [TextContent(
                type="text",
                text=json.dumps(response, ensure_ascii=False)
            )]

    async def run(self):
        """运行MCP服务器"""
        logger.info("启动ddddocr MCP服务器...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="ddddocr-mcp",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )

def main():
    """主函数"""
    server = DDDDOCRServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main() 