import gradio as gr
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# ✅ Set your API key
os.environ["GOOGLE_API_KEY"] = "API_KEY"  # Replace with your actual Gemini API key

# ✅ Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# ✅ Function to parse AI output and return clean HTML
def analyze_neuro_profile(user_input):
    prompt = f"""
You are a cognition profiling agent. The user is describing their mental behavior or struggles.

Your job is to:
1. Identify possible neurodiverse conditions (ADHD, Autism, Dyslexia, Anxiety, OCD, etc.)
2. For each, provide 1-line reasoning
3. State confidence level (Low / Medium / High)
4. Suggest what additional input could improve the diagnosis

Respond in this exact format:
---
Possible Conditions:
- ADHD (Medium): Trouble focusing in noisy spaces
- Dyslexia (Low): Avoids long paragraphs

Reasoning:
- Based on symptoms of focus issues and reading avoidance.

Suggestions:
- Ask about writing, memory, and childhood behavior.

Confidence:
Medium
---
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt + f"\nUser Input:\n{user_input}")])
        output = response.content.strip()

        # ✅ Convert plain text output into HTML
        html_response = "<div style='font-family:Arial; line-height:1.5;'>"
        for line in output.split("\n"):
            if line.startswith("- "):
                html_response += f"<li>{line[2:]}</li>"
            elif line.endswith(":") and not line.startswith("Confidence"):
                html_response += f"<h4 style='margin-top:10px;'>{line}</h4>"
            elif "Confidence" in line:
                html_response += f"<p><b>{line}</b></p>"
            else:
                html_response += f"<p>{line}</p>"
        html_response += "</div>"

        return html_response

    except Exception as e:
        return f"<p style='color:red;'>❌ Error: {str(e)}</p>"

# ✅ Gradio Interface with HTML output
ui = gr.Interface(
    fn=analyze_neuro_profile,
    inputs=gr.Textbox(
        label="📝 Describe user’s behavior / struggles",
        placeholder="e.g. I avoid eye contact and get distracted easily...",
        lines=4
    ),
    outputs=gr.HTML(label="🧠 Cognitive Profile Analysis"),
    title="🧠 Neurodiversity Cognition Screener",
    description="This tool analyzes user behavior and suggests possible neurodiverse conditions (ADHD, Autism, Anxiety, etc.) based on input.",
)

# ✅ Run app
if __name__ == "__main__":
    ui.launch()
