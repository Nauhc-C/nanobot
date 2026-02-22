# QQ 与飞书消息渠道配置完整指南

本指南将详细介绍如何为 nanobot 配置 QQ 和飞书消息渠道，以便接收闹钟提醒和其他消息。

## 目录
- [概述](#概述)
- [QQ 配置](#qq-配置)
- [飞书配置](#飞书配置)
- [闹钟提醒使用](#闹钟提醒使用)
- [常见问题](#常见问题)

---

## 概述

nanobot 支持多种消息渠道，其中 **QQ** 和 **飞书** 是最常用的两个平台。配置好这些渠道后，您的 nanobot 闹钟提醒就可以通过这些平台发送给您了。

### 功能对比

| 功能 | QQ | 飞书 |
|------|-----|------|
| 私聊消息 | ✅ | ✅ |
| 群聊消息 | ❌ | ✅ |
| WebSocket 连接 | ✅ | ✅ |
| 无需公网 IP | ✅ | ✅ |
| 富文本消息 | ❌ | ✅ |
| 消息反应 | ❌ | ✅ |

---

## QQ 配置

详细的 QQ 配置请参考 [[QQ消息配置指南]]，这里只列出关键步骤。

### 前置要求

1. **QQ 账号**
2. **Python 3.11+**
3. **qq-botpy 库**

### 快速配置步骤

#### 1. 安装依赖

```bash
pip install qq-botpy
```

#### 2. 注册 QQ 开放平台开发者

1. 访问 [QQ 开放平台](https://q.qq.com)
2. 登录并注册为开发者
3. 创建机器人应用
4. 获取 `AppID` 和 `AppSecret`

#### 3. 配置沙箱环境

在应用管理页面添加测试 QQ 号码到沙箱配置中。

#### 4. 编辑 nanobot 配置文件

打开 `~/.nanobot/config.json`，添加以下内容：

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "app_id": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allow_from": []
    }
  }
}
```

#### 5. 启动网关

```bash
nanobot gateway
```

#### 6. 测试连接

用手机 QQ 扫描机器人二维码，发送测试消息。

---

## 飞书配置

### 前置要求

1. **飞书账号**
2. **Python 3.11+**
3. **lark-oapi 库**

### 详细配置步骤

#### 1. 安装依赖

```bash
pip install lark-oapi
```

#### 2. 创建飞书机器人应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击"创建应用"
3. 选择"企业自建应用"
4. 填写应用信息：
   - 应用名称：例如 "nanobot 助手"
   - 应用描述：AI 助手
   - 应用图标：上传自定义头像
5. 点击"确定创建"

#### 3. 启用机器人能力

1. 在应用详情页，点击左侧"应用功能" → "机器人"
2. 点击"启用机器人"
3. 配置机器人信息：
   - 机器人名称：显示名称
   - 机器人描述：简要介绍
   - 机器人头像：上传头像

#### 4. 配置权限

1. 点击左侧"权限管理"
2. 添加以下权限：
   - `im:message` - 发送消息
   - `im:message.group` - 发送群消息（可选）

#### 5. 配置事件订阅

1. 点击左侧"事件订阅"
2. 点击"添加事件"
3. 选择 `im.message.receive_v1` - 接收消息
4. 选择"长连接"模式（重要！）

#### 6. 获取凭证

1. 点击左侧"凭证与基础信息"
2. 复制以下信息：
   - **App ID**（App ID）
   - **App Secret**（App Secret）

#### 7. 发布应用（重要！）

1. 点击左侧"版本管理与发布"
2. 点击"创建版本"
3. 填写版本信息
4. 点击"申请发布"
5. 等待审核通过（个人应用通常很快）

#### 8. 编辑 nanobot 配置文件

打开 `~/.nanobot/config.json`，添加以下内容：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxxxxxxxxxxxx",
      "appSecret": "xxxxxxxxxxxxxxxxxxxxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": []
    }
  }
}
```

**参数说明：**
- `enabled`：是否启用飞书通道
- `appId`：从飞书开放平台获取的 App ID
- `appSecret`：从飞书开放平台获取的 App Secret
- `encryptKey`：加密密钥（可选，长连接模式可留空）
- `verificationToken`：验证令牌（可选，长连接模式可留空）
- `allowFrom`：允许访问的用户 open_id 列表，空数组表示允许所有用户

#### 9. 启动网关

```bash
nanobot gateway
```

启动成功后，您会看到类似这样的输出：

```
Feishu bot started with WebSocket long connection
No public IP required - using WebSocket to receive events
```

#### 10. 测试连接

1. 打开飞书
2. 搜索您的机器人名称
3. 点击"开始聊天"
4. 发送一条测试消息，例如 "你好"
5. 等待机器人回复

---

## 闹钟提醒使用

配置好 QQ 或飞书后，您就可以使用 nanobot 设置闹钟提醒了。

### 方式 1：通过聊天界面

在 QQ 或飞书中向 nanobot 发送：

```
请在一个半小时后提醒我
```

或者更精确：

```
设置一个闹钟，在 2026-02-22T11:30:00 提醒我
```

### 方式 2：通过命令行

```bash
# 计算一个半小时后的时间
nanobot cron add --name "闹钟" --message "闹钟响了！" --at "2026-02-22T11:30:00" --deliver --channel "feishu" --to "your_open_id"
```

**参数说明：**
- `--name`：任务名称
- `--message`：提醒消息
- `--at`：ISO 格式的时间
- `--deliver`：发送到渠道
- `--channel`：渠道名称（qq 或 feishu）
- `--to`：接收者的 open_id

### 查看已设置的任务

```bash
nanobot cron list
```

---

## 常见问题

### QQ 相关问题

**Q: 为什么我收不到 QQ 消息？**

A: 请检查：
1. 是否在沙箱配置中添加了测试 QQ 号
2. AppID 和 AppSecret 是否正确
3. 应用是否已审核通过

**Q: 如何获取用户的 openid？**

A: 当用户向机器人发送消息时，nanobot 会在日志中输出 openid。

### 飞书相关问题

**Q: 飞书配置中 encryptKey 和 verificationToken 是必填的吗？**

A: 不是。使用 WebSocket 长连接模式时，这两个字段可以留空。

**Q: 如何获取用户的 open_id？**

A: 在飞书中向机器人发送消息，nanobot 会在日志中输出 sender_id，格式为 `ou_xxxxxxxxxx`。

**Q: 飞书机器人可以在群聊中使用吗？**

A: 可以。需要：
1. 将机器人添加到群聊
2. 在群聊中 @ 机器人
3. 确保配置了群聊相关权限

### 通用问题

**Q: 配置多个渠道时，闹钟会发送到哪个渠道？**

A: 这取决于您设置闹钟时指定的渠道。您可以同时配置多个渠道，然后在设置闹钟时选择要发送到哪个渠道。

**Q: nanobot 需要一直运行吗？**

A: 是的。为了让闹钟正常工作，`nanobot gateway` 需要保持运行状态。

**Q: 如何确保 nanobot 持续运行？**

A: 您可以使用：
- Windows：任务计划程序
- Linux/Mac：systemd 或 nohup
- Docker：docker-compose

---

## 技术参考

相关文件：
- QQ 实现：`nanobot/channels/qq.py`
- 飞书实现：`nanobot/channels/feishu.py`
- 配置定义：`nanobot/config/schema.py`
- 定时任务：`nanobot/cron/service.py`

相关文档：
- [[QQ消息配置指南]]
