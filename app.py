from flask import Flask, render_template, request, jsonify, send_file
from scanner import run_scan
from cert_gen import generate_cert
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_target():
    data = request.json
    target = data['target']
    tools = data['tools']
    
    # Update target CSV
    pd.DataFrame([[target, "pending"]]).to_csv('data/target.csv', mode='a', header=False, index=False)
    
    # Run scan
    results = run_scan(target, tools)
    
    # Update done CSV
    pd.DataFrame([[target, "completed"]]).to_csv('data/done.csv', mode='a', header=False, index=False)
    
    return jsonify(results=results)

@app.route('/generate-cert', methods=['POST'])
def generate_certificate():
    data = request.json
    name = data['name']
    identity = data['identity']
    course = data['course']
    
    cert_path = generate_cert(name, identity, course)
    return send_file(cert_path, as_attachment=True)

@app.route('/voice-command', methods=['POST'])
def voice_command():
    command = request.json['command'].lower()
    response = "Command executed"
    
    if 'scan' in command:
        response = "Starting security scan"
    elif 'read' in command:
        response = "Reading scan results"
    elif 'test' in command:
        response = "Running diagnostic tests"
    elif 'certificate' in command:
        response = "Generating PDF certificate"
    
    return jsonify(response=response)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)