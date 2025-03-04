from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

status = "WAIT"

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({'status': status})

@app.route('/run', methods=['POST'])
def run_script():
    global status
    if status == "WAIT":
        status = "START"
        subprocess.run(["/path/to/test.sh"])
        status = "DONE"
        return jsonify({'status': 'DONE'})
    return jsonify({'status': 'BUSY'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
