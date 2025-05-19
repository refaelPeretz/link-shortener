from flask import Flask, request, redirect, jsonify
import os
import json
import string
import random

app = Flask(__name__)
DATA_FILE = "data.json"

# Load existing data or start fresh
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        urls = json.load(f)
else:
    urls = {}

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")
    if not original_url:
        return jsonify({"error": "Missing URL"}), 400

    short_code = generate_short_code()
    while short_code in urls:
        short_code = generate_short_code()

    urls[short_code] = original_url
    with open(DATA_FILE, "w") as f:
        json.dump(urls, f)

    return jsonify({"short_url": request.host_url + short_code})

@app.route("/<short_code>")
def redirect_to_original(short_code):
    if short_code in urls:
        return redirect(urls[short_code])
    return "Short URL not found", 404

if __name__ == "__main__":
    app.run()
