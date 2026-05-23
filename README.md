# screenshot-translation

图片翻译后端服务，对接百度图片翻译 API，支持 API Key 鉴权和限流控制。

## 快速开始

### 本地运行

```bash
pip install fastapi uvicorn httpx pydantic-settings python-multipart

cp .env.example .env
# 编辑 .env，填入 BAIDU_APPID、BAIDU_TOKEN、API_KEYS

uvicorn app.main:app --reload
```

### Docker Compose 部署

```bash
# 创建 .env 文件（参考 .env.example）
docker compose up -d
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `BAIDU_APPID` | 百度翻译 AppID |
| `BAIDU_TOKEN` | 百度翻译 API Key（控制台 → APIKey管理） |
| `API_KEYS` | 内部鉴权 Key，逗号分隔，如 `sk-key1,sk-key2` |
| `RATE_LIMIT_PER_MINUTE` | 每个 Key 每分钟请求限制，默认 60 |
| `PORT` | 服务端口，默认 8000 |

## API

### 健康检查

```
GET /health
```

### 图片翻译

```
POST /api/v1/translate/image
Authorization: Bearer <api-key>
Content-Type: multipart/form-data

image   图片文件（必填）
from    源语言，支持 auto（必填）
to      目标语言（必填）
paste   贴合类型：0=不贴图，1=整图，2=块区，3=透明底图（默认 0）
```

**响应示例：**

```json
{
  "success": true,
  "data": {
    "from_lang": "en",
    "to_lang": "zh",
    "src": "原文全文...",
    "dst": "译文全文...",
    "contents": [
      {
        "src": "原文文本块",
        "dst": "译文文本块",
        "rect": "x,y,w,h",
        "line_count": 1,
        "points": [{"x": 0, "y": 0}],
        "paste_img": "base64图片（paste>0时返回）"
      }
    ]
  }
}
```

**错误响应：**

| 状态码 | 说明 |
|--------|------|
| 401 | API Key 无效或未提供 |
| 429 | 请求频率超限 |
| 502 | 百度 API 调用失败 |

## Docker

### 使用已发布镜像

```bash
docker pull mikukko/screenshot-translation:latest

docker run -d -p 8000:8000 \
  -e BAIDU_APPID=your-appid \
  -e BAIDU_TOKEN=your-token \
  -e API_KEYS=sk-your-key \
  mikukko/screenshot-translation:latest
```

镜像支持 `linux/amd64` 和 `linux/arm64`。

### 本地构建镜像

```bash
# 配置环境变量
cp .env.example .env
# 编辑 .env，填入实际的 BAIDU_APPID、BAIDU_TOKEN、API_KEYS

# 构建本地镜像
docker build -t screenshot-translation:local .

# 运行
docker run -d -p 8000:8000 --env-file .env screenshot-translation:local
```

### 多架构构建并推送

```bash
docker buildx create --use --name multiarch
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t your-dockerhub/screenshot-translation:latest \
  --push .
```
