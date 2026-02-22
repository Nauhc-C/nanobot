# B站API使用指南

## 1. 什么是B站API

B站API是哔哩哔哩网站提供的应用程序接口，允许开发者获取和操作B站的数据，包括用户信息、视频内容、动态信息等。

## 2. 获取B站API认证信息

### 2.1 获取Cookie

1. **登录B站网页版**：
   - 打开浏览器，访问 [https://www.bilibili.com](https://www.bilibili.com)
   - 登录您的B站账号

2. **打开开发者工具**：
   - 在浏览器中按 `F12` 打开开发者工具
   - 切换到 `网络` 或 `Network` 标签页

3. **刷新页面**：
   - 刷新B站首页，观察网络请求
   - 找到一个请求，查看其请求头中的 `Cookie` 字段

4. **复制Cookie**：
   - 复制完整的 `Cookie` 值，这将用于API请求的认证

### 2.2 必要的Cookie字段

在获取的Cookie中，以下字段是必须的：

- `SESSDATA`：会话数据，最重要的认证字段
- `bili_jct`：用于某些需要CSRF验证的操作
- `DedeUserID`：用户ID
- `DedeUserID__ckMd5`：用户ID的MD5值

## 3. 使用B站API获取用户动态

### 3.1 获取用户动态的API接口

**接口URL**：`https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| host_uid | string | 是 | 用户的B站UID |
| offset | string | 否 | 分页偏移量，用于加载更多动态 |
| size | string | 否 | 每页返回的动态数量，默认10 |

**请求头**：

```
Cookie: SESSDATA=your_sessdata_here; bili_jct=your_bili_jct_here; DedeUserID=your_user_id_here; DedeUserID__ckMd5=your_user_id_md5_here
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
```

### 3.2 示例代码

```python
import httpx

# 配置
headers = {
    "Cookie": "SESSDATA=your_sessdata_here; bili_jct=your_bili_jct_here",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# API参数
params = {
    "host_uid": "27867310",  # 目标用户的UID
    "size": "20"  # 每页返回20条动态
}

# 发送请求
url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=headers, params=params)
    data = response.json()

# 处理响应
if data.get("code") == 0:
    dynamics = data.get("data", {}).get("items", [])
    for dynamic in dynamics:
        # 提取动态信息
        pass
else:
    print(f"API请求失败: {data.get('message')}")
```

## 4. 解析B站动态数据

### 4.1 动态数据结构

B站动态API返回的JSON数据结构较为复杂，主要包含以下部分：

- `code`：返回码，0表示成功
- `message`：返回消息
- `data`：数据部分
  - `items`：动态列表
    - 每个动态包含 `modules`、`type`、`id_str` 等字段

### 4.2 提取动态信息

```python
def extract_dynamic_info(dynamic):
    """提取动态信息"""
    # 获取动态ID
    dynamic_id = dynamic.get("id_str", "")
    
    # 获取动态类型
    dynamic_type = dynamic.get("type", 0)
    
    # 获取发布时间
    modules = dynamic.get("modules", {})
    module_author = modules.get("module_author", {})
    publish_time = module_author.get("pub_ts", 0)
    
    # 获取动态内容
    module_dynamic = modules.get("module_dynamic", {})
    content = module_dynamic.get("desc", {}).get("text", "")
    
    # 获取图片信息
    pictures = []
    if "module_picture" in modules:
        module_picture = modules.get("module_picture", {})
        items = module_picture.get("items", [])
        for item in items:
            pictures.append(item.get("src", ""))
    
    # 获取视频信息
    video_info = {}
    if "module_video" in modules:
        module_video = modules.get("module_video", {})
        video_info = {
            "title": module_video.get("title", ""),
            "cover": module_video.get("cover", ""),
            "play_url": module_video.get("play_url", "")
        }
    
    return {
        "id": dynamic_id,
        "type": dynamic_type,
        "publish_time": publish_time,
        "content": content,
        "pictures": pictures,
        "video": video_info
    }
```

## 5. 集成到nanobot

### 5.1 创建B站动态获取技能

在 `~/.nanobot/workspace/skills/` 目录下创建 `bilibili` 文件夹，并添加以下文件：

#### `SKILL.md`

```markdown
---
name: bilibili
description: 获取B站用户动态
author: nanobot
version: 1.0.0
---

# B站动态获取技能

用于获取指定B站用户的动态信息。

## 使用方法

1. 配置B站Cookie
2. 使用 `bilibili_dynamic` 工具获取动态

## 工具

### bilibili_dynamic

获取B站用户动态。

**参数**：
- `uid`: B站用户UID
- `cookie`: B站登录Cookie
- `limit`: 限制返回数量

**返回**：
- 动态列表，包含发布时间、内容、图片等信息
```

### 5.2 创建B站动态获取工具

在 `nanobot/agent/tools/` 目录下创建 `bilibili.py` 文件：

```python
"""B站工具：获取B站用户动态。"""

import json
from typing import Any

import httpx

from nanobot.agent.tools.base import Tool


class BilibiliDynamicTool(Tool):
    """获取B站用户动态。"""
    
    name = "bilibili_dynamic"
    description = "获取B站用户动态，返回发布时间、内容、图片等信息。"
    parameters = {
        "type": "object",
        "properties": {
            "uid": {"type": "string", "description": "B站用户UID"},
            "cookie": {"type": "string", "description": "B站登录Cookie"},
            "limit": {"type": "integer", "description": "限制返回数量", "minimum": 1, "maximum": 50}
        },
        "required": ["uid", "cookie"]
    }
    
    async def execute(self, uid: str, cookie: str, limit: int = 20, **kwargs: Any) -> str:
        try:
            headers = {
                "Cookie": cookie,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            params = {
                "host_uid": uid,
                "size": str(limit)
            }
            
            url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, headers=headers, params=params, timeout=10.0)
                r.raise_for_status()
            
            data = r.json()
            
            if data.get("code") != 0:
                return json.dumps({"error": f"API请求失败: {data.get('message')}"})
            
            dynamics = data.get("data", {}).get("items", [])
            result = []
            
            for dynamic in dynamics:
                modules = dynamic.get("modules", {})
                module_author = modules.get("module_author", {})
                module_dynamic = modules.get("module_dynamic", {})
                
                dynamic_info = {
                    "id": dynamic.get("id_str", ""),
                    "type": dynamic.get("type", 0),
                    "publish_time": module_author.get("pub_ts", 0),
                    "content": module_dynamic.get("desc", {}).get("text", ""),
                    "pictures": [],
                    "video": {}
                }
                
                # 提取图片
                if "module_picture" in modules:
                    module_picture = modules.get("module_picture", {})
                    items = module_picture.get("items", [])
                    for item in items:
                        dynamic_info["pictures"].append(item.get("src", ""))
                
                # 提取视频
                if "module_video" in modules:
                    module_video = modules.get("module_video", {})
                    dynamic_info["video"] = {
                        "title": module_video.get("title", ""),
                        "cover": module_video.get("cover", "")
                    }
                
                result.append(dynamic_info)
            
            return json.dumps({"dynamics": result, "count": len(result)})
        except Exception as e:
            return json.dumps({"error": str(e)})
```

### 5.3 更新工具注册

在 `nanobot/agent/tools/__init__.py` 文件中添加：

```python
from .bilibili import BilibiliDynamicTool

__all__ = [
    # 其他工具
    "BilibiliDynamicTool"
]
```

## 6. 配置nanobot定时任务

### 6.1 创建定时任务

使用以下命令创建每周获取B站动态的任务：

```bash
python -m nanobot cron add --name "B站动态获取" --message "使用 bilibili_dynamic 工具获取 UID 为 27867310 的用户动态，Cookie 为 'your_cookie_here'，限制返回 20 条，然后按时间顺序整理成列表格式" --cron "0 9 * * 1"
```

### 6.2 查看任务状态

```bash
python -m nanobot cron list
```

### 6.3 测试任务执行

```bash
python -m nanobot cron run <job_id> --force
```

## 7. 注意事项

### 7.1 认证信息保护

- **不要**将Cookie信息硬编码在代码中
- **不要**在公共代码库中提交包含Cookie的文件
- 建议使用环境变量或配置文件存储Cookie信息

### 7.2 API使用限制

- B站API有访问频率限制，不要过于频繁地调用
- 建议将获取频率控制在合理范围内，如每小时或每天一次
- 如果遇到412、429等错误，表示触发了访问限制

### 7.3 动态类型处理

B站动态有多种类型，包括：
- 1: 普通动态
- 8: 转发动态
- 512: 视频动态
- 1024: 图文动态
- 2048: 文字动态
- 4096: 音频动态

不同类型的动态数据结构可能不同，需要分别处理。

## 8. 常见问题

### 8.1 API请求失败

**症状**：返回错误码非0
**原因**：
- Cookie过期或无效
- 触发了B站的访问限制
- 参数错误
**解决方案**：
- 更新Cookie
- 降低访问频率
- 检查请求参数

### 8.2 无法获取动态内容

**症状**：返回的动态列表为空
**原因**：
- 用户未发布动态
- Cookie权限不足
- API版本变更
**解决方案**：
- 检查用户是否有动态
- 确保Cookie包含正确的权限
- 参考最新的API文档

### 8.3 动态类型识别错误

**症状**：无法正确识别或处理某些类型的动态
**原因**：
- 动态类型较多，处理逻辑不完整
- API返回的数据结构发生变化
**解决方案**：
- 完善动态类型处理逻辑
- 定期更新API调用代码

## 9. 参考资料

- [B站开放平台](https://open.bilibili.com)
- [B站API文档](https://github.com/SocialSisterYi/bilibili-API-collect)
- [Python httpx文档](https://www.python-httpx.org)

## 10. 总结

使用B站API获取用户动态是一个可行的方案，通过正确配置认证信息和API参数，可以获取到完整的用户动态数据。将其集成到nanobot中，可以实现定期自动获取B站动态并发送通知的功能。

需要注意的是，B站API可能会随时变更，需要定期关注API文档的更新，以确保代码的兼容性。同时，要遵守B站的使用规则，不要滥用API，以免被限制访问。