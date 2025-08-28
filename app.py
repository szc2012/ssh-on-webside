from flask import Flask, render_template, request, jsonify
import paramiko
import json
import os

app = Flask(__name__)

# Load SSH config from config.json
with open('config.json') as f:
    config = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

# 全局变量存储SSH会话
ssh_client = None
ssh_channel = None

@app.route('/ssh/connect', methods=['POST'])
def ssh_connect():
    global ssh_client, ssh_channel
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=config['host'],
            port=config['port'],
            username=config['username'],
            password=config['password'],
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