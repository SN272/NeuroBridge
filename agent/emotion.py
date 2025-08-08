import os
import sys
import google.generativeai as genai
from transformers import pipeline
from flask import Flask, request, jsonify, Response
from datetime import datetime


# --- Emotion Agent Class ---
class EmotionAgent:
    """
    An agent that detects a user's emotional state from text and
    adapts its conversational tone accordingly using an LLM.
    """
    def __init__(self, api_key: str):
        print("Initializing Emotion Agent...")
        if not api_key:
            raise ValueError("Google API Key not found.")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        try:
            print("Loading emotion detection model...")
            self.emotion_classifier = pipeline(
                "text-classification", 
                model="michellejieli/emotion_text_classifier"
            )
            print("Emotion Agent is ready.")
        except Exception as e:
            print(f"Error loading Hugging Face model: {e}", file=sys.stderr)
            sys.exit(1)

    def detect_emotion(self, text: str) -> str:
        try:
            results = self.emotion_classifier(text)
            return results[0]['label']
        except Exception as e:
            print(f"Could not classify emotion: {e}", file=sys.stderr)
            return "neutral"

    def adapt_and_respond(self, user_input: str) -> tuple[str, str]:
        detected_emotion = self.detect_emotion(user_input)
        tone_guidelines = {
            'sadness': "Respond with empathy, gentleness, and support.",
            'joy': "Share in their happiness! Respond with a celebratory and positive tone.",
            'anger': "Respond with a calm, patient, and de-escalating tone.",
            'fear': "Respond with a reassuring and calming tone.",
            'surprise': "Respond with curiosity and engagement.",
            'disgust': "Respond with a neutral, understanding tone.",
            'neutral': "Respond in a standard, helpful, and friendly tone."
        }
        instructional_prompt = tone_guidelines.get(detected_emotion, tone_guidelines['neutral'])
        final_prompt = f"""
        **System Role:** You are a caring AI assistant. Your goal is to be understanding and empathetic.
        **Tone and Style Guideline:** {instructional_prompt}
        **User's Message:** "{user_input}"
        **Your Response:**
        """
        try:
            response = self.gemini_model.generate_content(final_prompt)
            return response.text.strip(), detected_emotion
        except Exception as e:
            print(f"Error calling Gemini API: {e}", file=sys.stderr)
            return "I'm having trouble connecting right now.", "neutral"


# --- HTML Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Agent</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f172a;
            color: #cbd5e1;
        }
        .chat-container {
            background-color: #1e293b;
            border: 1px solid #334155;
        }
        .chat-bubble {
            padding: 12px 16px;
            border-radius: 16px;
            max-width: 75%;
        }
        .agent-bubble {
            background-color: #334155;
            border-bottom-left-radius: 4px;
            color: #e2e8f0;
        }
        .user-bubble {
            background-color: #7c3aed;
            color: white;
            border-bottom-right-radius: 4px;
        }
        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            background-color: #475569;
            flex-shrink: 0;
        }
        .timestamp {
            font-size: 0.75rem;
            color: #64748b;
            margin-top: 4px;
        }
        .input-area {
            background-color: #0f172a;
            border-top: 1px solid #334155;
        }
        .header-border {
            border-bottom: 1px solid #334155;
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-4xl mx-auto chat-container rounded-2xl shadow-2xl flex flex-col h-[90vh]">
        <!-- Header -->
        <div class="p-6 header-border flex items-center space-x-4">
            <div class="avatar text-lg">😊</div>
            <div>
                <h1 class="text-xl font-bold text-white">Emotion Agent</h1>
                <p class="text-sm text-slate-400">AI that understands and adapts to your emotions</p>
            </div>
        </div>
        
        <!-- Chat Area -->
        <div id="chat-area" class="flex-1 p-6 overflow-y-auto space-y-4">
            <!-- Initial Message -->
            <div class="flex items-start space-x-3">
                <div class="avatar">😊</div>
                <div class="flex-1">
                    <div class="agent-bubble">
                        Hello! I'm your Emotion Agent. I can detect emotions in your messages and respond with empathy and understanding. How are you feeling today?
                    </div>
                    <div class="timestamp text-left" id="initial-timestamp">03:27 PM</div>
                </div>
            </div>
        </div>
        
        <!-- Input Area -->
        <div class="input-area p-6">
            <div class="flex items-center space-x-3">
                <input 
                    type="text" 
                    id="user-input" 
                    class="flex-1 px-4 py-3 bg-slate-700 border border-slate-600 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-slate-400" 
                    placeholder="Share your thoughts and feelings..."
                >
                <button 
                    id="send-button" 
                    class="bg-purple-600 text-white rounded-full p-3 hover:bg-purple-700 transition-colors"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <script>
        const chatArea = document.getElementById('chat-area');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');

        function formatTime() {
            return new Date().toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: true 
            });
        }

        // Set initial timestamp
        document.getElementById('initial-timestamp').textContent = formatTime();

        function addMessage(message, sender, emotion = 'neutral') {
            const messageWrapper = document.createElement('div');
            const avatar = document.createElement('div');
            const bubbleWrapper = document.createElement('div');
            const bubble = document.createElement('div');
            const timestamp = document.createElement('div');

            const emotionAvatars = {
                sadness: '😢', 
                joy: '😄', 
                anger: '😠', 
                fear: '😰', 
                surprise: '😮', 
                disgust: '😒',
                neutral: '🙂'
            };

            avatar.className = 'avatar';
            bubbleWrapper.className = 'flex-1';
            bubble.textContent = message;
            timestamp.className = 'timestamp';
            timestamp.textContent = formatTime();

            if (sender === 'user') {
                messageWrapper.className = 'flex items-start flex-row-reverse space-x-3 space-x-reverse';
                bubble.className = 'user-bubble';
                avatar.textContent = emotionAvatars[emotion] || '🙂';
                timestamp.classList.add('text-right');
            } else {
                messageWrapper.className = 'flex items-start space-x-3';
                bubble.className = 'agent-bubble';
                avatar.textContent = '😊';
                timestamp.classList.add('text-left');
            }
            
            bubbleWrapper.appendChild(bubble);
            bubbleWrapper.appendChild(timestamp);
            messageWrapper.appendChild(avatar);
            messageWrapper.appendChild(bubbleWrapper);
            chatArea.appendChild(messageWrapper);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        async function handleSend() {
            const message = userInput.value.trim();
            if (!message) return;
            
            userInput.value = '';
            userInput.disabled = true;
            sendButton.disabled = true;

            try {
                const response = await fetch('/get_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                
                // Add user message with detected emotion avatar
                addMessage(message, 'user', data.emotion);
                
                // Add agent response
                addMessage(data.response, 'agent');
                
            } catch (error) {
                console.error("Error:", error);
                addMessage("Sorry, something went wrong on the server.", 'agent');
            } finally {
                userInput.disabled = false;
                sendButton.disabled = false;
                userInput.focus();
            }
        }

        sendButton.addEventListener('click', handleSend);
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') handleSend();
        });

        // Focus input on load
        userInput.focus();
    </script>
</body>
</html>
"""

# --- Flask Web Server ---
app = Flask(__name__)

# Initialize the agent
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: The GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
    print("Please set your Google API key: export GOOGLE_API_KEY='AIzaSyBQPdYspFjp2y-cOGMp7QwIuYPGbyJGzI8'")
    sys.exit(1)

emotion_agent = EmotionAgent(api_key=api_key)

@app.route('/')
def home():
    """Serves the main HTML page."""
    return Response(HTML_TEMPLATE, mimetype='text/html')

@app.route('/get_response', methods=['POST'])
def get_response():
    """Handles API requests from the JavaScript front-end."""
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get the response and detected emotion from the agent
    agent_response, detected_emotion = emotion_agent.adapt_and_respond(user_message)
    
    return jsonify({
        'response': agent_response, 
        'emotion': detected_emotion
    })

if __name__ == '__main__':
    print("Starting Emotion Agent server...")
    print("Open your browser and go to http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
