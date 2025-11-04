# 服务器端实现（使用 FastAPI，异步性能更优）
from fastapi import FastAPI, StreamingResponse
import asyncio
import json
import time
from typing import AsyncGenerator

app = FastAPI()


class StreamableHTTPMCPServer:
    def __init__(self):
        self.tools = {}
        self.sessions = {}

    def generate_tokens(self, prompt: str) -> list:
        """模拟 LLM token 生成（实际场景替换为真实 LLM 调用）"""
        mock_response = f"基于 prompt '{prompt}' 生成的流式响应："
        return [char for char in mock_response]  # 按字符拆分模拟 token 流

    async def stream_response(self, request: dict) -> StreamingResponse:
        """流式 HTTP 响应核心接口（分块返回 LLM 输出）"""

        async def generate_stream() -> AsyncGenerator[str, None]:
            prompt = request.get('prompt', '默认prompt')

            # 1. 发送初始元数据（第一块数据）
            yield json.dumps({
                'type': 'metadata',
                'timestamp': time.time(),
                'prompt': prompt
            }) + '\n'  # 换行符用于客户端分割块

            # 2. 流式返回 LLM 生成的 token（后续块）
            for token in self.generate_tokens(prompt):
                yield json.dumps({
                    'type': 'token',
                    'content': token,
                    'timestamp': time.time()
                }) + '\n'
                await asyncio.sleep(0.05)  # 模拟 LLM 生成延迟（实际场景移除）

            # 3. 发送结束标记（最后一块数据）
            yield json.dumps({
                'type': 'end',
                'timestamp': time.time(),
                'status': 'complete'
            }) + '\n'

        # 配置流式响应头（关键：Transfer-Encoding: chunked 由 FastAPI 自动添加）
        return StreamingResponse(
            generate_stream(),
            media_type='application/x-ndjson',  # 新行分隔 JSON，便于客户端解析
            headers={
                'Cache-Control': 'no-cache',         # 禁用缓存
                'X-Accel-Buffering': 'no',           # 禁用反向代理缓冲（如 Nginx）
                'Access-Control-Allow-Origin': '*'
            }
        )


server = StreamableHTTPMCPServer()


@app.post("/mcp/stream")
async def stream_endpoint(request: dict):
    return await server.stream_response(request)


@app.get("/mcp/health")
async def health_check():
    """服务健康检查接口（非流式辅助接口）"""
    return {
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': time.time(),
        'support_transport': 'streamable_http'
    }