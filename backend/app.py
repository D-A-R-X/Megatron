from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "AI Smart Assistant Suite Backend Running 🚀"})

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    try:
        # Run the local Ollama model
        result = subprocess.run(
            ["ollama", "run", "phi3"],
            input=user_input.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode('utf-8').strip()
        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/automation', methods=['POST'])
def automation():
    task = request.json.get('task', '').lower()

    if 'open notepad' in task:
        subprocess.Popen(['notepad.exe'])
        return jsonify({"status": "✅ Notepad opened"})

    elif 'open browser' in task:
        subprocess.Popen(['start', 'chrome'], shell=True)
        return jsonify({"status": "🌐 Chrome opened"})

    elif 'shutdown' in task:
        subprocess.run(["shutdown", "/s", "/t", "10"])
        return jsonify({"status": "⚠️ System will shutdown in 10 seconds"})

    else:
        return jsonify({"status": f"🤖 Unknown automation task: {task}"})

if __name__ == '__main__':
    app.run(debug=True)
