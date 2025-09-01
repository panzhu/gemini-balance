# Gemini Balance - iFlow CLI 使用指南

## 项目概述

Gemini Balance 是一个基于 Python FastAPI 构建的 Gemini API 代理和负载均衡器。该项目提供以下核心功能：

- **多密钥负载均衡**: 支持配置多个 Gemini API 密钥进行自动轮询
- **双协议 API 兼容**: 同时支持 Gemini 和 OpenAI CHAT API 格式
- **图像文本聊天与修改**: 支持图像生成和编辑功能
- **Web 搜索**: 集成网络搜索功能
- **密钥状态监控**: 提供实时密钥状态监控界面
- **详细日志记录**: 完整的错误日志和请求日志系统

## 技术栈

- **后端框架**: FastAPI + Uvicorn
- **数据库**: MySQL / SQLite
- **API 客户端**: httpx, google-genai, openai
- **配置管理**: pydantic-settings, python-dotenv
- **任务调度**: APScheduler
- **模板引擎**: Jinja2

## 构建和运行

### Docker Compose (推荐)

```bash
# 复制环境配置文件
cp .env.example .env
# 编辑 .env 文件配置数据库和 API 密钥
# 启动服务
docker-compose up -d
```

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件进行配置

# 启动开发服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 生产环境部署

```bash
# 使用 Docker
docker run -d -p 8000:8000 --name gemini-balance \
  -v ./data:/app/data \
  --env-file .env \
  ghcr.io/snailyp/gemini-balance:latest
```

## 关键命令

### 开发命令
```bash
# 启动开发服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 运行测试
python -m pytest tests/

# 代码格式化 (如果配置了)
python -m black app/
python -m isort app/
```

### Docker 命令
```bash
# 查看日志
docker logs gemini-balance

# 重启服务
docker restart gemini-balance

# 进入容器
docker exec -it gemini-balance bash
```

## 项目结构

```
app/
├── config/           # 配置管理
├── core/            # 核心应用逻辑
├── database/        # 数据库模型和连接
├── domain/          # 业务领域对象
├── exception/       # 自定义异常
├── handler/         # 请求处理器
├── log/             # 日志配置
├── middleware/      # FastAPI 中间件
├── router/          # API 路由
├── scheduler/       # 定时任务
├── service/         # 业务逻辑服务
├── static/          # 静态文件
├── templates/       # HTML 模板
└── utils/           # 工具函数
```

## API 端点

### Gemini 格式 API (`/gemini/v1beta`)
- `GET /models` - 列出可用模型
- `POST /models/{model}:generateContent` - 生成内容
- `POST /models/{model}:streamGenerateContent` - 流式生成内容

### OpenAI 兼容格式
- `GET /hf/v1/models` - 列出模型 (Hugging Face 兼容)
- `POST /hf/v1/chat/completions` - 聊天补全
- `POST /hf/v1/embeddings` - 文本嵌入
- `POST /hf/v1/images/generations` - 图像生成

### 标准 OpenAI 格式
- `GET /openai/v1/models` - 列出模型
- `POST /openai/v1/chat/completions` - 聊天补全
- `POST /openai/v1/embeddings` - 文本嵌入
- `POST /openai/v1/images/generations` - 图像生成

## 配置说明

关键环境变量配置 (在 `.env` 文件中设置):

```env
# 必需配置
API_KEYS=key1,key2,key3           # Gemini API 密钥
ALLOWED_TOKENS=token1,token2      # 访问令牌

# 数据库配置
DATABASE_TYPE=mysql               # 或 sqlite
MYSQL_HOST=localhost
MYSQL_USER=username
MYSQL_PASSWORD=password
MYSQL_DATABASE=gemini_balance

# 可选功能配置
IMAGE_MODELS=gemini-2.0-flash-exp  # 支持图像生成的模型
SEARCH_MODELS=gemini-2.0-flash-exp # 支持网络搜索的模型
PROXIES=http://proxy:port         # 代理服务器
```

## 开发约定

### 代码风格
- 使用 Python 3.9+ 语法特性
- 遵循 PEP 8 代码规范
- 使用类型注解
- 模块化设计，遵循单一职责原则

### 测试实践
- 单元测试位于 `tests/` 目录
- 使用 pytest 测试框架
- 测试覆盖核心业务逻辑

### 日志规范
- 使用结构化日志记录
- 不同模块使用不同的 logger
- 日志级别: DEBUG, INFO, WARNING, ERROR

## 故障排除

### 常见问题
1. **数据库连接失败**: 检查 MySQL 服务状态和连接参数
2. **API 密钥无效**: 确认 Gemini API 密钥有效且有配额
3. **端口冲突**: 检查 8000 端口是否被占用
4. **依赖安装失败**: 确保 Python 版本 >= 3.9

### 日志查看
```bash
# Docker 容器日志
docker logs gemini-balance

# 应用日志文件
cat data/logs/app.log
```

## 扩展开发

### 添加新功能
1. 在 `app/service/` 创建新的服务类
2. 在 `app/router/` 添加对应的路由
3. 在 `app/domain/` 定义相关数据模型
4. 更新配置管理 (如需要)

### 自定义中间件
在 `app/middleware/` 目录中添加自定义中间件，并在 `app/core/application.py` 中注册。

## 许可证

本项目采用 [CC BY-NC 4.0](LICENSE) 许可证，禁止商业转售服务。

---

*最后更新: 2025-09-01*