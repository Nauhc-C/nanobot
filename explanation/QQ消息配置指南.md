# nanobot QQ 消息功能配置指南

## 1. 功能概述

nanobot 支持通过 QQ 平台发送和接收消息，具体功能包括：

- ✅ 接收 QQ 私聊消息
- ✅ 发送 QQ 私聊消息
- ✅ 自动重连机制
- ✅ 消息去重处理
- ❌ 暂不支持群聊消息

## 2. 依赖项

nanobot 使用 botpy SDK 与 QQ 开放平台进行交互，因此需要安装以下依赖：

```bash
pip install qq-botpy
```

## 3. 配置步骤

### 3.1 在 QQ 开放平台注册开发者账号

1. 访问 [QQ 开放平台](https://q.qq.com)
2. 点击右上角 "登录" 按钮，使用 QQ 账号登录
3. 登录后，点击 "注册开发者"，选择个人开发者或企业开发者
4. 按照提示完成开发者认证流程

### 3.2 创建 QQ 机器人应用

1. 登录 QQ 开放平台后，进入 [应用管理](https://q.qq.com/wiki/tools/dev/devcenter/application/apply.html) 页面
2. 点击 "创建应用"，选择 "机器人" 类型
3. 填写应用基本信息：
   - 应用名称：填写你的机器人名称
   - 应用描述：简要描述机器人功能
   - 应用图标：上传机器人头像
   - 应用类型：选择 "聊天机器人"
4. 点击 "提交审核"，等待审核通过

### 3.3 获取 AppID 和 AppSecret

1. 应用审核通过后，进入应用详情页
2. 点击左侧菜单 "开发设置"
3. 在 "基本信息" 部分，找到并复制：
   - AppID：机器人的唯一标识
   - AppSecret：机器人的密钥（注意保密）

### 3.4 配置沙箱环境（测试用）

1. 在应用详情页，找到 "沙箱配置" 部分
2. 点击 "在消息列表配置" 下的 "添加成员"
3. 输入你要用于测试的 QQ 号码，点击 "添加"
4. 保存配置

### 3.5 配置 nanobot

1. 打开 nanobot 配置文件 `~/.nanobot/config.json`
2. 在 `channels` 部分添加 QQ 配置：

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

**参数说明：**
- `enabled`：是否启用 QQ 通道
- `app_id`：从 QQ 开放平台获取的 AppID
- `secret`：从 QQ 开放平台获取的 AppSecret
- `allow_from`：允许访问的用户 openid 列表，空数组表示允许所有用户

### 3.6 启动 nanobot 网关

```bash
nanobot gateway
```

## 4. 测试和验证

### 4.1 连接测试

1. 启动 nanobot 网关后，查看终端输出，确认 QQ 机器人已启动：
   ```
   QQ bot started (C2C private message)
   ```

2. 使用手机 QQ 扫描机器人的二维码，打开机器人资料页
3. 点击 "发消息"，向机器人发送一条测试消息
4. 查看 nanobot 终端输出，确认收到消息
5. 等待机器人回复，验证消息发送功能

### 4.2 获取用户 openid

当用户向机器人发送消息时，nanobot 会在日志中记录用户的 openid。如果你需要限制访问权限，可以：

1. 让测试用户向机器人发送一条消息
2. 查看 nanobot 终端日志，找到类似以下输出：
   ```
   Handling message from user: openid_1234567890
   ```
3. 将该 openid 添加到 `allow_from` 列表中：

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "app_id": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allow_from": ["openid_1234567890"]
    }
  }
}
```

4. 重启 nanobot 网关使配置生效

## 5. 生产环境部署

### 5.1 提交审核

1. 在 QQ 开放平台应用详情页，点击 "提交审核"
2. 填写审核信息：
   - 应用介绍：详细描述机器人功能
   - 使用场景：说明机器人的使用场景
   - 隐私政策：提供机器人的隐私政策链接
   - 服务条款：提供机器人的服务条款链接
3. 上传相关证明材料（如需要）
4. 点击 "提交"，等待审核通过

### 5.2 发布应用

1. 审核通过后，进入应用详情页
2. 点击 "发布应用"
3. 选择发布范围（公开或指定用户）
4. 点击 "确认发布"

## 6. 常见问题和解决方案

### 6.1 QQ SDK 未安装

**错误信息：**
```
QQ SDK not installed. Run: pip install qq-botpy
```

**解决方案：**
```bash
pip install qq-botpy
```

### 6.2 AppID 或 AppSecret 未配置

**错误信息：**
```
QQ app_id and secret not configured
```

**解决方案：**
确保在 `config.json` 中正确配置了 `app_id` 和 `secret` 参数。

### 6.3 无法收到消息

**可能原因：**
1. 沙箱环境未添加测试用户
2. 网络连接问题
3. QQ 机器人审核未通过

**解决方案：**
1. 检查沙箱配置，确保已添加测试用户
2. 检查网络连接，确保能正常访问 QQ 开放平台
3. 检查应用审核状态，确保已审核通过

### 6.4 无法发送消息

**可能原因：**
1. AppSecret 错误
2. 机器人权限不足
3. 网络连接问题

**解决方案：**
1. 检查 AppSecret 是否正确
2. 确保机器人已获取发送消息的权限
3. 检查网络连接，确保能正常访问 QQ 开放平台

## 7. 技术实现细节

nanobot 的 QQ 功能通过以下文件实现：

- `nanobot/channels/qq.py`：QQ 通道的核心实现
- `nanobot/config/schema.py`：QQ 配置的 schema 定义

### 7.1 核心功能

1. **消息接收**：通过 botpy SDK 的 WebSocket 连接接收消息
2. **消息发送**：使用 `post_c2c_message` API 发送私聊消息
3. **自动重连**：当连接断开时，自动尝试重新连接
4. **消息去重**：使用 deque 存储已处理的消息 ID，避免重复处理

### 7.2 配置结构

QQ 配置的结构定义如下：

```python
class QQConfig(BaseModel):
    """QQ channel configuration using botpy SDK."""
    enabled: bool = False
    app_id: str = ""  # 机器人 ID (AppID) from q.qq.com
    secret: str = ""  # 机器人密钥 (AppSecret) from q.qq.com
    allow_from: list[str] = Field(default_factory=list)  # Allowed user openids (empty = public access)
```

## 8. 总结

nanobot 提供了完整的 QQ 消息功能支持，通过以下步骤即可完成配置：

1. 在 QQ 开放平台注册开发者账号并创建机器人应用
2. 获取 AppID 和 AppSecret
3. 配置沙箱环境进行测试
4. 在 nanobot 配置文件中添加 QQ 配置
5. 启动 nanobot 网关
6. 测试消息发送和接收功能
7. 提交审核并发布应用（生产环境）

通过以上步骤，你可以成功配置 nanobot 的 QQ 消息功能，实现通过 QQ 与 nanobot 进行交互。