from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS for frontend requests

# Load GPT-2 model and tokenizer
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Explicitly set pad_token
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

@app.route("/")
def home():
    """Render the chatbot UI"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user input and generate GPT-2 response"""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"response": "Invalid request. Please send a valid message."}), 400

    prompt = f"User: {data['message']}\nChatbot: "  # Structure like a chatbot conversation
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    with torch.no_grad():
        gen_tokens = model.generate(
            input_ids,
            max_length=100,  # Keep responses short and concise
            temperature=0.5,  # Lower = less randomness (more focused answers)
            top_p=0.8,  # Reduce randomness further (keep responses meaningful)
            top_k=30,  # Smaller top_k for more deterministic responses
            repetition_penalty=1.5,  # Stronger penalty to avoid repetition
            do_sample=True,  # Still allow some variety
            num_return_sequences=1,  # Generate only one response
            pad_token_id=tokenizer.pad_token_id  # Avoid padding warnings
        )

    gen_text = tokenizer.decode(gen_tokens[0], skip_special_tokens=True)

    # Ensure response is clean by removing 'User:' and keeping only chatbot reply
    bot_response = gen_text.replace(prompt, "").strip()

    return jsonify({"response": bot_response}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
