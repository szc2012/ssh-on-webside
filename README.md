以下是优化后的项目文档，在保持简洁性的同时增强了清晰度、安全性提示和用户体验：

# SSH on WebSide

## 项目描述
一个轻量级的基于Web的SSH客户端，让用户可通过浏览器便捷、安全地连接和管理远程服务器，无需安装本地SSH客户端。

## 安装指南

### 前置要求
- Python 3.6+
- 网络连接（用于安装依赖）

### 步骤
1. 克隆项目仓库：
   ```bash
   git clone https://github.com/szc2012/ssh-on-webside.git
   cd ssh-on-webside
   ```

2. 推荐：创建并激活虚拟环境（避免依赖冲突）
   ```bash
   # 创建虚拟环境（可选）
   python -m venv venv
   
   # 激活虚拟环境
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
   > 依赖说明：`flask`（Web框架）、`paramiko`（SSH协议实现）


## 使用说明

### 配置服务器信息
1. 复制配置模板（避免直接修改示例文件）：
2. 编辑`config.json`文件，填入服务器信息：
   ```json
   {
       "host": "192.168.100.10",  // 远程服务器IP或域名
       "port": 22,                // SSH端口（默认22）
       "username": "your_name",   // SSH用户名
       "password": "your_pwd"     // SSH密码
   }
   ```


### 启动与访问
1. 启动应用：
   ```bash
   python app.py
   ```

2. 在浏览器中访问：
   ```
   http://localhost:8000
   ```

3. 成功连接后，即可在Web界面中执行SSH命令管理服务器。


## 安全提示
- **生产环境注意**：
  - 不要将`config.json`提交到代码仓库（已加入`.gitignore`）
  - 建议启用HTTPS加密传输（可配合Nginx或Flask-Talisman实现）
  - 限制访问来源，避免公网直接暴露


## 贡献指南
欢迎参与项目改进：
1. Fork本仓库
2. 创建特性分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add some amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 打开Pull Request


## 许可证
本项目基于 [MIT License](LICENSE) 开源。