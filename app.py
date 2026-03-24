from flask import Flask, render_template, request, jsonify
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load models and vectorizer
try:
    mlp_model = joblib.load('neural_network_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print("Models loaded successfully")
except FileNotFoundError as e:
    print(f"Error loading models: {e}")
    mlp_model = None
    vectorizer = None

# Load dataset with responses
try:
    df = pd.read_csv('Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv')
    print(f"Dataset loaded: {len(df)} records")
except FileNotFoundError:
    print("Warning: CSV file not found. Default responses will be used.")
    df = None

# Preprocess text function
def preprocess_text(text):
    """Preprocess user input text"""
    if text is None:
        return ""
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token.strip() for token in tokens if token.strip()]
    return ' '.join(tokens)

# Predict intent function
def predict_intent(user_input):
    """Predict the intent of user input"""
    if not mlp_model or not vectorizer:
        return "greeting", "I'm here to help! Please try your question again."
    
    try:
        preprocessed = preprocess_text(user_input)
        if not preprocessed:
            return "greeting", "I didn't understand that. Could you please rephrase?"
        
        user_input_vec = vectorizer.transform([preprocessed])
        prediction = mlp_model.predict(user_input_vec)[0]
        return prediction, get_response(prediction)
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "error", "Sorry, I encountered an error. Please try again."

# Get response based on intent
def get_response(intent):
    """Get response based on predicted intent"""
    if df is not None:
        # Filter responses by intent
        responses = df[df['intent'] == intent]['response'].tolist()
        if responses:
            return random.choice(responses)
    
    # Default responses
    default_responses = {
        'greeting': "Hello! How can I help you today?",
        'goodbye': "Thank you for chatting with me. Have a great day!",
        'help': "I'm here to assist you. What do you need help with?",
        'complaint': "I'm sorry to hear that. Let me help you resolve this issue.",
        'suggestion': "Thank you for your feedback!",
    }
    
    return default_responses.get(intent, "I'm here to help. What can I do for you?")

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    intent, bot_response = predict_intent(user_message)
    
    return jsonify({
        'intent': intent,
        'response': bot_response
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    # For local testing
    app.run(debug=True, host='0.0.0.0', port=5000)
