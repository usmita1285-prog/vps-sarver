import os
import json
import random
import string
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"servers": []}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"servers": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/vps/list', methods=['GET'])
def list_vps():
    return jsonify(load_data())

@app.route('/api/vps/create', methods=['POST'])
def create_vps():
    req = request.json or {}
    username = req.get('username', 'client').strip().lower()
    ram = req.get('ram', '1024 MB')
    cores = req.get('cores', '1 Core')
    disk = req.get('disk', '10 GB')

    vps_id = str(random.randint(1000, 9999))
    vps_ip = f"51.21.131.{random.randint(10, 250)}"
    ssh_port = 2200 + int(vps_id) % 100
    
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(12))

    new_vps = {
        "id": vps_id,
        "username": username,
        "ip": vps_ip,
        "ssh_port": ssh_port,
        "ssh_command": f"ssh -p {ssh_port} {username}@{vps_ip}",
        "password": password,
        "ram": ram,
        "cores": cores,
        "disk": disk,
        "status": "Active"
    }

    db = load_data()
    db["servers"].append(new_vps)
    save_data(db)

    return jsonify({"success": True, "vps": new_vps})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
