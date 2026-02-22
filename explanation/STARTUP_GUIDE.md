# nanobot 启动指南

本文档详细介绍如何启动和运行 nanobot 个人 AI 助手。

## 前置条件

1. **Python 环境**：需要 Python ≥ 3.11
2. **API Key**：需要配置 LLM 提供商的 API Key（如 OpenRouter、OpenAI 等）
3. **配置文件**：已完成初始化和配置

## 启动方式

### 1. 命令行交互模式

这是最基本的启动方式，直接在终端中与 nanobot 交互。

**步骤**：
1. 确保已完成初始化配置：
   ```bash
   nanobot onboard
   ```

2. 配置 API Key（在 `~/.nanobot/config.json` 中）：
   ```json
   {
     "providers": {
       "openrouter": {
         "apiKey": "sk-or-v1-xxx"
       }
     },
     "agents": {
       "defaults": {
         "model": "anthropic/claude-opus-4-5"
       }
     }
   }
   ```

3. 启动交互模式：
   ```bash
   nanobot agent
   ```

4. 开始聊天：
   ```
   > 你好，帮我分析一下今天的天气
   ```

**退出方式**：输入 `exit`、`quit`、`/exit`、`/quit`、`:q` 或按 `Ctrl+D`

**高级选项**：
- 一次性命令：`nanobot agent -m "你好，帮我分析一下今天的市场趋势"`
- 纯文本模式：`nanobot agent --no-markdown`
- 显示日志：`nanobot agent --logs`

### 2. 聊天应用网关模式

通过各种聊天应用（如 Telegram、Discord、飞书等）与 nanobot 交互。

**步骤**：
1. 配置聊天应用（以 Telegram 为例）：
   ```json
   {
     "channels": {
       "telegram": {
         "enabled": true,
         "token": "YOUR_BOT_TOKEN",
         "allowFrom": ["YOUR_USER_ID"]
       }
     }
   }
   ```

2. 启动网关：
   ```bash
   nanobot gateway
   ```

3. 在聊天应用中开始对话

**支持的聊天应用**：
- Telegram
- Discord
- WhatsApp
- Feishu (飞书)
- Mochat (Claw IM)
- DingTalk (钉钉)
- Slack
- Email
- QQ

### 3. 定时任务模式

设置周期性任务，让 nanobot 自动执行。

**添加任务**：
```bash
# 每天早上9点执行
nanobot cron add --name "daily" --message "早上好！今天有什么计划？" --cron "0 9 * * *"

# 每小时执行一次
nanobot cron add --name "hourly" --message "检查系统状态" --every 3600
```

**管理任务**：
```bash
# 列出所有任务
nanobot cron list

# 移除任务
nanobot cron remove <job_id>
```

### 4. Docker 模式

使用 Docker 容器运行 nanobot。

**步骤**：
1. 构建镜像：
   ```bash
   docker build -t nanobot .
   ```

2. 初始化配置：
   ```bash
   docker run -v ~/.nanobot:/root/.nanobot --rm nanobot onboard
   ```

3. 编辑配置文件（在主机上）：
   ```bash
   vim ~/.nanobot/config.json
   ```

4. 运行网关：
   ```bash
   docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 nanobot gateway
   ```

5. 运行单个命令：
   ```bash
   docker run -v ~/.nanobot:/root/.nanobot --rm nanobot agent -m "Hello!"
   ```

## 常见问题

### 1. 启动失败 - API Key 错误

**症状**：启动时显示 API Key 无效或认证失败

**解决方案**：
- 检查 API Key 是否正确
- 确保 API Key 格式符合提供商要求
- 检查网络连接是否正常

### 2. 聊天应用无响应

**症状**：启动网关后，聊天应用中 nanobot 无响应

**解决方案**：
- 检查聊天应用的配置是否正确
- 确保聊天应用的 token 有效
- 检查网络连接是否正常
- 查看日志输出获取更多信息

### 3. 响应速度慢

**症状**：nanobot 响应时间过长

**解决方案**：
- 使用更强大的模型
- 调整配置文件中的参数：
  ```json
  {
    "agents": {
      "defaults": {
        "maxTokens": 4096,  // 减少令牌数
        "temperature": 0.3   // 降低温度
      }
    }
  }
  ```

### 4. 工具执行失败

**症状**：nanobot 无法执行文件操作或命令

**解决方案**：
- 检查权限设置
- 确保工作目录正确
- 如需限制工作区：
  ```json
  {
    "tools": {
      "restrictToWorkspace": true
    }
  }
  ```

## 状态检查

使用以下命令检查 nanobot 的状态：

```bash
nanobot status
```

## 故障排除

1. **查看日志**：
   ```bash
   nanobot agent --logs
   ```

2. **检查配置**：
   ```bash
   cat ~/.nanobot/config.json
   ```

3. **重新初始化**：
   ```bash
   # 备份配置
   cp ~/.nanobot/config.json ~/.nanobot/config.json.bak
   # 重新初始化
   nanobot onboard
   ```

## 最佳实践

1. **使用 OpenRouter**：推荐使用 OpenRouter 作为提供商，它提供了多种模型的访问
2. **合理配置**：根据你的硬件和网络情况调整配置参数
3. **安全第一**：设置用户白名单和工作区限制
4. **定期更新**：保持 nanobot 版本最新以获得新功能和修复

## 联系方式

如果遇到问题，可以通过以下渠道获取帮助：
- GitHub Issues：https://github.com/HKUDS/nanobot/issues
- Discord 社区：https://discord.gg/MnCvHqpUGB
- 飞书群组：查看项目 README.md
- 微信群组：查看项目 README.md
