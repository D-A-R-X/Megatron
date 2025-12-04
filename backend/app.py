# backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='/static')
CORS(app)

def scrape_quotes_sample():
    """Scrapes first quote from quotes.toscrape.com and returns a short string."""
    url = "https://quotes.toscrape.com"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        first = soup.select_one(".quote")
        if first:
            text = first.select_one(".text").get_text(strip=True)
            author = first.select_one(".author").get_text(strip=True)
            return f'"{text}" — {author}'
        return "No quotes found."
    except Exception as e:
        return f"Scrape failed: {e}"

def simulate_send_email(recipient, subject, body):
    """Simulates sending email. For expo we just log to console and return success."""
    # If you want real email later, replace this with smtplib logic and SMTP credentials (careful).
    print("=== Simulated Email ===")
    print("To:", recipient)
    print("Subject:", subject)
    print("Body:", body[:200])
    print("=======================")
    return True

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/run', methods=['POST'])
def run_flow():
    data = request.json
    logs = []
    step = 1
    visual_files = []
    total_steps = len(data.get("actions", []))
    user_input = data.get("input", "")

    if "collect_reports" in data.get("actions", []):
        logs.append(f"[{step}/{total_steps}] Collecting report: {user_input}...")
        visual_files.append(f"{user_input}.csv")
        logs.append(f"Report {user_input}.csv downloaded ✅")
        step += 1

    if "analyze_data" in data.get("actions", []):
        logs.append(f"[{step}/{total_steps}] Analyzing data from {user_input}.csv ...")
        logs.append(f"Analysis complete: All checks passed ✅")
        step += 1

    if "send_notification" in data.get("actions", []):
        logs.append(f"[{step}/{total_steps}] Sending notification email ... ✅")
        step += 1

    if "save_logs" in data.get("actions", []):
        logs.append(f"[{step}/{total_steps}] Saving logs and reports ...")
        logs.append(f"Logs and files saved: {', '.join(visual_files)} ✅")
        step += 1

    logs.append("Workflow complete ✅")
    return jsonify({
    "logs": logs or [],
    "files": visual_files or []
})


if __name__ == '__main__':
    app.run(debug=True)