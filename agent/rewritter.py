# Rewriter Agent
import os
import subprocess
import sys
import time

required_packages = [
    "Flask==2.2.5",
    "flask-cors==3.0.10",
    "google-generativeai==0.3.2"
]

for package in required_packages:
    try:
        __import__(package.split("==")[0].replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# =========================
# Gemini API Configuration
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "API KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set your GEMINI_API_KEY environment variable.")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# =========================
# Embedded HTML Page
# =========================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Rewriter Agent</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex justify-center items-center min-h-screen p-4">
  <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-2xl">
    <h1 class="text-3xl font-bold mb-6 text-center text-blue-700">Rewriter Agent</h1>

    <label class="block mb-2 font-semibold text-gray-700">Original Text:</label>
    <textarea id="originalText" class="w-full p-3 border rounded mb-4" placeholder="Enter your text or upload a .txt file..."></textarea>

    <input type="file" id="fileUpload" accept=".txt" class="mb-4 w-full" />

    <button id="rewriteButton" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Rewrite</button>

    <label class="block mt-6 mb-2 font-semibold text-gray-700">Rewritten Text:</label>
    <textarea id="rewrittenText" class="w-full p-3 border rounded bg-gray-100" readonly></textarea>

    <button id="downloadButton" class="w-full mt-4 bg-green-600 text-white py-2 rounded hover:bg-green-700">Download as .txt</button>
  </div>

  <script>
    const button = document.getElementById('rewriteButton');
    const inputText = document.getElementById('originalText');
    const outputText = document.getElementById('rewrittenText');
    const fileUpload = document.getElementById('fileUpload');
    const downloadBtn = document.getElementById('downloadButton');

    fileUpload.addEventListener('change', () => {
      const file = fileUpload.files[0];
      if (file && file.type === "text/plain") {
        const reader = new FileReader();
        reader.onload = (e) => {
          inputText.value = e.target.result;
        };
        reader.readAsText(file);
      } else {
        alert("Please upload a valid .txt file.");
      }
    });

    button.addEventListener('click', async () => {
      const text = inputText.value.trim();
      if (!text) return alert("Please enter some text.");

      button.textContent = "Rewriting...";
      button.disabled = true;

      try {
        const response = await fetch('/rewrite', {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });

        const data = await response.json();
        outputText.value = data.rewritten_text || "Error occurred.";
      } catch (err) {
        outputText.value = "Failed to connect to server.";
      }

      button.textContent = "Rewrite";
      button.disabled = false;
    });

    downloadBtn.addEventListener('click', () => {
      const text = outputText.value;
      if (!text) {
        alert("No rewritten text to download.");
        return;
      }
      const blob = new Blob([text], { type: "text/plain" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "rewritten_text.txt";
      link.click();
    });
  </script>
</body>
</html>
"""

# =========================
# Routes
# =========================
@app.route("/rewrite", methods=["POST"])
def rewrite_text():
    """Rewrite the provided text to a 6th-grade reading level."""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided in the request body."}), 400

    original_text = data["text"]
    prompt = f"Rewrite the following passage to a 6th-grade reading level:\n\n{original_text}"

    try:
        for i in range(5):
            try:
                response = model.generate_content(prompt)
                rewritten_text = response.text
                return jsonify({"rewritten_text": rewritten_text}), 200
            except Exception:
                time.sleep(2 ** i)
        raise Exception("Max retries exceeded")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    """Serve the HTML UI."""
    return HTML_PAGE

# =========================
# Run App
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
