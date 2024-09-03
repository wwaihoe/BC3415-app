from flask import Flask, render_template, request, jsonify
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=os.path.abspath('static'))

import google.generativeai as genai
import textblob

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="You are a financial advisor helping a client with their finance questions.",
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)


# Sample FAQs
faqs = [
    {
        "question": "How much should I save for retirement?",
        "answer": "A general rule of thumb is to save 10-15% of your income for retirement. However, the exact amount depends on your age, lifestyle, and retirement goals."
    },
    {
        "question": "What is the importance of diversification in investing?",
        "answer": "Diversification helps spread risk across different types of investments, potentially reducing the impact of poor performance in any single investment on your overall portfolio."
    },
    {
        "question": "How can I improve my credit score?",
        "answer": "To improve your credit score, pay bills on time, keep credit card balances low, avoid opening too many new accounts, and regularly check your credit report for errors."
    }
]

# Sample jokes
jokes = [
    {
        "question": "Why did the banker switch careers?",
        "answer": "Because he lost interest!"
    },
    {
        "question": "Why was the bond so excited to go to the party?",
        "answer": "It heard it would be a real interest-ing time!"
    },
    {
        "question": "Why did the stock market break up with the economy?",
        "answer": "It couldn’t handle the constant ups and downs!"
    }
]


@app.route('/')
def index():
    return render_template('index.html', faqs=faqs)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    chat_session = model.start_chat(
        history=[]
    )
    user_message = request.json['message'].lower()
    response = chat_session.send_message(user_message)
    return jsonify({'response': response.text})

@app.route('/financejokes')
def financejokes():
    return render_template('jokes.html', jokes=jokes)

@app.route('/sentimentanalysis')
def sentimentanalysis():
    return render_template('sentiment_analysis.html')

@app.route('/sentimentanalysisquery', methods=['POST'])
def sentimentanalysisquery():
    text = request.json['text']
    sentiment = textblob.TextBlob(text).sentiment
    return jsonify({'polarity': sentiment.polarity, 'subjectivity': sentiment.subjectivity})

if __name__ == '__main__':
    app.run(debug=True)