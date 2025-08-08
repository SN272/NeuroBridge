from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Example agent launcher
@app.route('/run/cognition')
def run_cognition():
    return launch_agent('agent/cognition.py')

@app.route('/run/emotion')
def run_emotion():
    return launch_agent('agent/emotion.py')

@app.route('/run/planner')
def run_planner():
    return launch_agent('agent/plan.py')

@app.route('/run/rewritter')
def run_rewritter():
    return launch_agent('agent/rewritter.py')

@app.route('/run/tutor')
def run_tutor():
    return launch_agent('agent/tutor.py')

@app.route('/run/progress')
def run_progress():
    return launch_agent('agent/progress.py')





def launch_agent(script_path):
    abs_path = os.path.join(os.path.dirname(__file__), script_path)
    if not os.path.exists(abs_path):
        return jsonify({"error": f"Agent not found: {abs_path}"}), 404
    subprocess.Popen(["python", abs_path])
    return jsonify({"status": "success", "message": f"Launching {os.path.basename(script_path)}"})

if __name__ == '__main__':
    app.run(debug=True)
