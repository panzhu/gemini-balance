"""请求频率限制服务"""

import time
import asyncio
from typing import Dict, Optional
from collections import defaultdict
from app.config.config import settings
from app.log.logger import get_rate_limiter_logger

logger = get_rate_limiter_logger()

class RateLimiter:
    """基于模型的速率限制器"""
    
    def __init__(self):
        # 模型速率限制配置 (RPM - Requests Per Minute)
        self.model_limits = {
            "gemini-2.5-pro": 5,  # 每分钟5次请求
            "gemini-2.5-flash": 10,  # 每分钟10次请求
            "gemini-2.5-flash-lite": 10,  # 每分钟10次请求
            # 默认限制
            "default": 5
        }
        
        # 为每个模型维护请求时间戳队列
        self.request_timestamps: Dict[str, list] = defaultdict(list)
        self.locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        
    def _get_model_limit(self, model: str) -> int:
        """获取模型的RPM限制"""
        # 清理模型名称，移除后缀
        clean_model = model
        if model.endswith("-search"):
            clean_model = model[:-7]
        if model.endswith("-image"):
            clean_model = model[:-6]
        if model.endswith("-non-thinking"):
            clean_model = model[:-13]
            
        return self.model_limits.get(clean_model, self.model_limits["default"])
    
    async def acquire(self, model: str) -> None:
        """获取令牌，如果需要则等待"""
        model_limit = self._get_model_limit(model)
        async with self.locks[model]:
            now = time.time()
            # 清理1分钟前的请求记录
            self.request_timestamps[model] = [
                timestamp for timestamp in self.request_timestamps[model] 
                if now - timestamp < 60
            ]
            
            # 检查是否超过限制
            if len(self.request_timestamps[model]) >= model_limit:
                # 计算需要等待的时间
                oldest_timestamp = self.request_timestamps[model][0]
                wait_time = 60 - (now - oldest_timestamp)
                if wait_time > 0:
                    logger.info(f"Rate limit reached for model {model}, waiting {wait_time:.2f} seconds")
                    await asyncio.sleep(wait_time)
                    # 等待后再次清理过期记录
                    now = time.time()
                    self.request_timestamps[model] = [
                        timestamp for timestamp in self.request_timestamps[model] 
                        if now - timestamp < 60
                    ]
            
            # 记录当前请求时间戳
            self.request_timestamps[model].append(now)
            logger.debug(f"Acquired rate limit token for model {model}, current count: {len(self.request_timestamps[model])}")

# 创建全局速率限制器实例
rate_limiter = RateLimiter()