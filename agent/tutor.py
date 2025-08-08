import tkinter as tk
from tkinter import messagebox, scrolledtext
import time # For simulating processing time
import google.generativeai as genai # Import the Google Generative AI library
import os # To access environment variables for the API key

# --- Configure your Gemini API Key ---
# IMPORTANT: Replace 'YOUR_GEMINI_API_KEY' with your actual API key.
# It's highly recommended to load this from an environment variable for security.
# Example: os.getenv("GEMINI_API_KEY")
# If running locally, you might set it directly like:
# GEMINI_API_KEY = "YOUR_API_KEY_HERE"
# You can get an API key from Google AI Studio: https://ai.google.dev/
API_KEY = os.getenv("GEMINI_API_KEY", "YOURAPIKEY") # Replace with your key or set as env var

# Configure the Generative AI model
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    print("Please ensure your API_KEY is valid and correctly set.")

class TutorAgentApp:
    def __init__(self, master):
        self.master = master
        master.title("✨ Your Enthusiastic Tutor Agent! ✨")
        master.geometry("800x650") # Set a default window size
        master.resizable(True, True) # Allow window resizing
        master.configure(bg="#e0f7fa") # Light blue background

        # --- Header ---
        self.header_frame = tk.Frame(master, bg="#00796b", pady=15)
        self.header_frame.pack(fill="x")
        self.header_label = tk.Label(self.header_frame, text="🧠 Let's Learn Something Amazing! 🚀",
                                     font=("Comic Sans MS", 22, "bold"), fg="white", bg="#00796b")
        self.header_label.pack()

        # --- Input Section ---
        self.input_frame = tk.Frame(master, bg="#b2dfdb", padx=20, pady=20, bd=3, relief="groove")
        self.input_frame.pack(pady=25, padx=30, fill="x")

        # Subject Input
        self.subject_label = tk.Label(self.input_frame, text="What subject sparks your curiosity today?",
                                      font=("Arial", 14, "bold"), bg="#b2dfdb", fg="#004d40")
        self.subject_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.subject_entry = tk.Entry(self.input_frame, width=45, font=("Arial", 13), bd=2, relief="solid")
        self.subject_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.subject_entry.insert(0, "e.g., Physics") # Placeholder text

        # Topic Input
        self.topic_label = tk.Label(self.input_frame, text="And what specific topic are we exploring?",
                                    font=("Arial", 14, "bold"), bg="#b2dfdb", fg="#004d40")
        self.topic_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.topic_entry = tk.Entry(self.input_frame, width=45, font=("Arial", 13), bd=2, relief="solid")
        self.topic_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.topic_entry.insert(0, "e.g., Black Holes") # Placeholder text

        self.input_frame.grid_columnconfigure(1, weight=1) # Allow entry fields to expand

        # --- Action Button ---
        self.explain_button = tk.Button(master, text="✨ Get My Simplified Explanation! ✨", command=self.get_explanation,
                                        font=("Arial", 16, "bold"), bg="#ff5722", fg="white",
                                        activebackground="#ff7043", activeforeground="white",
                                        relief="raised", bd=6, cursor="hand2", padx=20, pady=10)
        self.explain_button.pack(pady=30)

        # --- Explanation Output Section ---
        self.output_frame = tk.Frame(master, bg="#ffffff", padx=15, pady=15, bd=3, relief="sunken")
        self.output_frame.pack(pady=10, padx=30, fill="both", expand=True)

        self.output_label = tk.Label(self.output_frame, text="Your Super Simplified Scoop:",
                                     font=("Arial", 15, "bold"), fg="#333333", bg="#ffffff")
        self.output_label.pack(pady=5)

        self.explanation_display = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, font=("Verdana", 12),
                                                             bg="#f8f8f8", fg="#222222", bd=2, relief="flat",
                                                             padx=15, pady=15, state="disabled")
        self.explanation_display.pack(fill="both", expand=True)

        # Initialize the Gemini model
        self.model = None
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        except Exception as e:
            messagebox.showerror("Model Error", f"Failed to load Gemini model. Please check your API key and network connection: {e}")

    def generate_simplified_content(self, subject, topic):
        """
        Generates simplified content using the Gemini API.
        """
        if not self.model:
            return "Oops! The AI model isn't ready. Please check your API key setup."

        prompt = f"""
        Explain the topic '{topic}' in the subject of '{subject}' in the most simplified way possible.
        Imagine you are explaining it to someone who is new to the topic.
        Use clear, concise language and avoid overly technical jargon.
        Include enthusiasm and use emojis where appropriate to make it engaging.
        Keep the explanation relatively brief, around 100-200 words.
        """

        try:
            # Simulate a little processing delay before sending to API
            time.sleep(0.5)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"""
            Oh no! I ran into a bit of a snag while trying to fetch that information. 😔
            It looks like there might be an issue with connecting to the AI service or
            processing your request.

            Here's what happened: {e}

            Please double-check your API key and your internet connection,
            then give it another try! You've got this! 💪
            """

    def get_explanation(self):
        """
        Retrieves subject and topic, then displays the simplified explanation.
        """
        subject = self.subject_entry.get().strip()
        topic = self.topic_entry.get().strip()

        if not subject or not topic:
            messagebox.showwarning("Input Error", "Oops! Please enter both a subject AND a topic to get started! 🤔")
            return

        # Clear previous text and show a "thinking" message
        self.explanation_display.config(state="normal")
        self.explanation_display.delete(1.0, tk.END)
        self.explanation_display.insert(tk.END, f"Thinking hard to simplify '{topic}' in '{subject}' for you... just a moment! 🤔\n\n")
        self.explanation_display.config(state="disabled")
        self.master.update_idletasks() # Update GUI to show message immediately

        # Get the simplified content
        simplified_info = self.generate_simplified_content(subject, topic)

        # Display the content
        self.explanation_display.config(state="normal")
        self.explanation_display.delete(1.0, tk.END) # Clear thinking message
        self.explanation_display.insert(tk.END, simplified_info)
        self.explanation_display.config(state="disabled")

def main():
    root = tk.Tk()
    app = TutorAgentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()