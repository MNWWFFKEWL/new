from flask import Flask, request, jsonify, send_from_directory
import os
import json
from pathlib import Path
from .data_processor import extract_features

app = Flask(__name__, static_folder='../frontend')
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "dataset.json"


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/add', methods=['POST'])
def add_entry():
    content = request.json.get('text', '')
    features = extract_features(content)
    data = load_data()
    data.append({'text': content, 'features': features})
    save_data(data)
    return jsonify({'status': 'ok', 'features': features})

@app.route('/api/dataset')
def dataset():
    return jsonify(load_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
