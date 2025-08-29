# SSH Web 客户端

通过浏览器实现 SSH 连接。

## 功能
- 通过 Web 界面连接远程服务器
- 支持主机地址、端口、用户名和密码配置
- 实时终端交互

## 安装
1. 克隆项目：
   ```bash
   git clone https://github.com/szc2012/ssh-on-webside.git
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行
启动 Flask 应用：
```bash
python app.py
```

## 使用
1. 访问 `http://localhost:8000`
2. 填写 SSH 配置并点击“连接”
3. 在终端中交互

## 依赖
- Flask
- Paramiko
- Gunicorn（可选）

## 技术实现方法

### 开放API接口

#### 1. 建立SSH连接
```plaintext
POST /api/connect
参数: {
  "host": "目标主机",
  "port": 22,
  "username": "用户名",
  "password": "密码" 或 "privateKey": "密钥内容"
}
返回: {
  "status": "success/error",
  "sessionId": "会话ID",
  "message": "连接成功/失败原因"
}
```

#### 2. 执行远程命令
```plaintext
POST /api/command
参数: {
  "sessionId": "会话ID",
  "command": "要执行的命令"
}
返回: {
  "status": "success/error",
  "output": "命令输出",
  "exitCode": 0
}
```

#### 3. 关闭连接
```plaintext
POST /api/disconnect
参数: {
  "sessionId": "会话ID"
}
返回: {
  "status": "success",
  "message": "连接已关闭"
}
```

### 前端实现
- **核心组件**：
  - 使用Xterm.js实现浏览器终端模拟
  ```javascript
  // 初始化Xterm终端
  const term = new Terminal({
    fontSize: 14,
    cursorBlink: true
  });
  term.open(document.getElementById('terminal'));
  ```
  - 基于HTML5构建交互界面
  ```html
  <div id="terminal"></div>
  <input type="text" id="command-input" />
  ```
  - TailwindCSS进行响应式布局
  ```css
  #terminal {
    @apply w-full h-96 bg-black text-white p-4;
  }
  ```

### 后端架构
- **连接层**：
  - Paramiko库处理SSH协议
  ```python
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(hostname, username=username, password=password)
  ```
  - 支持密码和密钥认证
  ```python
  # 密钥认证示例
  pkey = paramiko.RSAKey.from_private_key_file('key.pem')
  ssh.connect(hostname, username=username, pkey=pkey)
  ```

### 通信机制
- **WebSocket实时通信**：
  ```python
  @socketio.on('message')
  def handle_message(data):
      emit('response', {'output': execute_command(data['cmd'])})
  ```

### 安全实现
- **会话隔离**：
  ```python
  sessions = {}  # 存储各会话的SSH连接
  ```

### 扩展接口
- **插件系统**：
  ```python
  def load_plugins():
      for plugin in plugins:
          plugin.register()
  ```