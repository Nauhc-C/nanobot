# B站动态获取功能使用文档

## 1. 功能概述

B站动态获取是 nanobot 的一项功能，用于定期获取指定 B 站用户的最新动态，并将结果整理成易于阅读的格式。

### 主要特点

- **定期自动获取**：每周一上午9点自动执行
- **多API接口支持**：自动切换多个API接口以提高可靠性
- **完整数据提取**：获取动态的发布时间、内容、图片、视频等信息
- **灵活配置**：可根据需求调整执行频率和数据处理方式

## 2. 技术实现

### 2.1 核心组件

- **B站动态获取工具**：`nanobot/agent/tools/bilibili.py`
  - 实现了获取用户信息和动态的功能
  - 支持多个API接口的自动切换
  - 处理不同数据结构的响应

- **定时任务服务**：`nanobot/cron/service.py`
  - 管理和执行定时任务
  - 支持cron表达式配置执行时间
  - 提供任务状态监控

### 2.2 数据流程

1. **定时触发**：cron服务在指定时间触发任务
2. **工具调用**：nanobot调用bilibili工具获取动态
3. **API请求**：发送请求到B站API获取数据
4. **数据处理**：解析API返回的数据
5. **结果存储**：将结果存储到会话文件中
6. **可选通知**：根据配置发送通知

## 3. 配置步骤

### 3.1 环境准备

1. **安装依赖**：
   ```bash
   pip install httpx typer prompt-toolkit pydantic pydantic-settings loguru
   ```

2. **创建虚拟环境**：
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

### 3.2 工具配置

1. **创建B站动态获取工具**：
   - 文件：`nanobot/agent/tools/bilibili.py`
   - 实现了获取用户信息和动态的功能

2. **更新工具注册**：
   - 文件：`nanobot/agent/tools/__init__.py`
   - 添加 `BilibiliTool` 到导入和 `__all__` 列表

### 3.3 定时任务配置

1. **添加定时任务**：
   ```bash
   python -m nanobot cron add --name "B站动态获取" --message "获取B站用户 27867310 的最新动态" --cron "0 9 * * 1"
   ```

2. **查看任务状态**：
   ```bash
   python -m nanobot cron list
   ```

3. **测试任务执行**：
   ```bash
   python -m nanobot cron run <job_id> --force
   ```

## 4. 使用方法

### 4.1 手动触发

```bash
python -m nanobot cron run f1edbbe6 --force
```

### 4.2 查看执行结果

1. **会话文件**：
   - 位置：`~/.nanobot/sessions/cli_direct.jsonl`
   - 包含完整的执行结果和数据

2. **记忆文件**：
   - 位置：`~/.nanobot/workspace/memory/`
   - 记录任务执行的历史

### 4.3 调整执行频率

修改定时任务的cron表达式：

- 每周一上午9点：`0 9 * * 1`
- 每天上午9点：`0 9 * * *`
- 每小时执行：`0 * * * *`

## 5. 数据结构

### 5.1 获取到的动态数据结构

```json
{
  "type": "dynamic",
  "data": [
    {
      "id": "动态ID",
      "type": "动态类型",
      "publish_time": "发布时间戳",
      "content": "动态内容",
      "pictures": ["图片URL1", "图片URL2"],
      "video": {
        "title": "视频标题",
        "cover": "视频封面URL"
      }
    },
    // 更多动态...
  ]
}
```

### 5.2 动态类型说明

- **1**：普通动态
- **8**：转发动态
- **512**：视频动态
- **1024**：图文动态
- **2048**：文字动态
- **4096**：音频动态

## 6. 常见问题及解决方案

### 6.1 API请求失败

**症状**：任务执行失败，返回错误信息
**原因**：
- Cookie过期或无效
- 触发了B站的访问限制
- API接口变更
**解决方案**：
- 更新Cookie
- 降低访问频率
- 检查API接口是否变更

### 6.2 无法获取动态内容

**症状**：返回的动态列表为空
**原因**：
- 用户未发布动态
- Cookie权限不足
- API参数错误
**解决方案**：
- 检查用户是否有动态
- 确保Cookie包含正确的权限
- 检查API参数配置

### 6.3 数据格式错误

**症状**：获取到的数据格式不符合预期
**原因**：
- B站API返回的数据结构变更
- 工具代码未及时更新
**解决方案**：
- 更新工具代码以适应新的数据结构
- 检查API文档了解变更

## 7. 后续优化建议

### 7.1 功能优化

1. **添加通知功能**：
   - 配置任务时添加 `--deliver` 参数
   - 设置通知渠道和接收人

2. **增加数据存储**：
   - 实现动态数据的持久化存储
   - 支持历史动态的查询和分析

3. **优化错误处理**：
   - 添加更完善的错误处理机制
   - 实现自动重试功能

### 7.2 性能优化

1. **减少API调用**：
   - 实现缓存机制
   - 避免重复获取相同数据

2. **并行处理**：
   - 对多个用户的动态获取实现并行处理
   - 提高处理效率

3. **资源管理**：
   - 优化内存使用
   - 合理设置超时时间

## 8. 配置示例

### 8.1 基本配置

```bash
# 添加每周一上午9点执行的任务
python -m nanobot cron add --name "B站动态获取" --message "获取B站用户 27867310 的最新动态" --cron "0 9 * * 1"
```

### 8.2 带通知的配置

```bash
# 添加带通知的任务
python -m nanobot cron add --name "B站动态获取" --message "获取B站用户 27867310 的最新动态" --cron "0 9 * * 1" --deliver --to "your_chat_id" --channel "telegram"
```

### 8.3 调整执行频率

```bash
# 每天上午9点执行
python -m nanobot cron add --name "B站动态获取" --message "获取B站用户 27867310 的最新动态" --cron "0 9 * * *"

# 每小时执行
python -m nanobot cron add --name "B站动态获取" --message "获取B站用户 27867310 的最新动态" --cron "0 * * * *"
```

## 9. 故障排查

### 9.1 检查任务状态

```bash
# 查看所有任务
python -m nanobot cron list

# 查看任务执行历史
# 检查会话文件中的执行记录
```

### 9.2 测试API连接

```python
import httpx

# 测试用户信息API
url = "https://api.bilibili.com/x/space/acc/info"
params = {"mid": "27867310"}
headers = {
    "Cookie": "your_cookie_here",
    "User-Agent": "Mozilla/5.0"
}

async def test_api():
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

import asyncio
asyncio.run(test_api())
```

### 9.3 查看日志

- 检查nanobot的运行日志
- 查看定时任务的执行日志
- 分析API请求的响应日志

## 10. 总结

B站动态获取功能为用户提供了一种自动、定期获取指定B站用户动态的方法，通过简单的配置即可实现自动化监控。该功能具有以下优势：

- **自动化**：无需手动操作，定期自动执行
- **可靠性**：多API接口支持，提高获取成功率
- **灵活性**：可根据需求调整配置
- **可扩展性**：易于添加新功能和优化性能

通过本文档的指导，用户可以轻松配置和使用B站动态获取功能，及时了解指定用户的最新动态。

## 11. 版本历史

- **v1.0.0**：初始版本
  - 实现基本的B站动态获取功能
  - 支持定时任务配置
  - 支持多API接口切换

- **v1.0.1**：优化版本
  - 改进错误处理机制
  - 优化数据存储方式
  - 增加文档说明

---

*文档创建时间：2026年2月18日*
*适用版本：nanobot v0.1.0+*
