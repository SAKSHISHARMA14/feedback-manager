from flask import Flask, request, redirect, url_for, render_template
import json, os

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "feedback.json")

# Ensure folder and file exist
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def read_feedback():
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_feedback(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)

@app.route("/")
def index():
    feedbacks = read_feedback()
    return render_template("index.html", feedbacks=feedbacks)

@app.route("/submit", methods=["POST"])
def submit():
    text = request.form.get("feedback", "").strip()
    if not text:
        return "Feedback is required", 400
    items = read_feedback()
    items.append(text)
    write_feedback(items)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
