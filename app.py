from flask import Flask, render_template, request, jsonify
import paramiko
import json
import os

app = Flask(__name__)

# 全局变量存储SSH配置和会话
ssh_config = {
    'host': '',
    'port': 22,
    'username': '',
    'password': ''
}
ssh_client = None
ssh_channel = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ssh')
def ssh_page():
    return render_template('index.html')

@app.route('/ssh/configure', methods=['POST'])
def ssh_configure():
    global ssh_config
    data = request.json
    ssh_config['host'] = data.get('host', '')
    ssh_config['port'] = data.get('port', 22)
    ssh_config['username'] = data.get('username', '')
    ssh_config['password'] = data.get('password', '')
    return jsonify({'status': 'success'})

@app.route('/ssh/connect', methods=['POST'])
def ssh_connect():
    global ssh_client, ssh_channel, ssh_config
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=ssh_config['host'],
            port=ssh_config['port'],
            username=ssh_config['username'],
            password=ssh_config['password'],
            timeout=10
        )
        ssh_channel = ssh_client.invoke_shell()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/ssh/read', methods=['GET'])
def ssh_read():
    global ssh_channel
    if ssh_channel and ssh_channel.recv_ready():
        data = ssh_channel.recv(1024).decode('utf-8')
        return jsonify({'status': 'success', 'data': data})
    return jsonify({'status': 'success', 'data': ''})

@app.route('/ssh/write', methods=['POST'])
def ssh_write():
    global ssh_channel
    message = request.json.get('message', '')
    if ssh_channel:
        ssh_channel.send(message)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'SSH channel not established'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
