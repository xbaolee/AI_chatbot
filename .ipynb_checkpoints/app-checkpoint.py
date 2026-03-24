from flask import Flask, render_template, request, jsonify
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import random

import nbformat
from nbconvert import PythonExporter

# Load the Jupyter notebook
with open('chatbotUI.ipynb') as f:
    notebook_content = f.read()

# Convert the notebook to a Python script
nb = nbformat.reads(notebook_content, as_version=4)
exporter = PythonExporter()
source, _ = exporter.from_notebook_node(nb)

# Execute the Python code in the notebook
exec(source)

# Now labeled_data will be available in this script if defined in the notebook

# Initialize the lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load the trained MLP model and TF-IDF vectorizer from the file
mlp_model = joblib.load('neural_network_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Preprocess function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token.strip() for token in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

# Preprocess input function
def preprocess_input(user_input):
    if user_input is None:
        raise ValueError("User input is None")
    preprocessed_input = preprocess_text(user_input)
    if preprocessed_input is None:
        raise ValueError("Preprocessed input is None")
    user_input_vec = vectorizer.transform([preprocessed_input])
    return user_input_vec

# Function to generate response based on the model prediction
def generate_response(prediction):
    responses = [item['response'] for item in labeled_data if item['label'] == prediction]
    if responses:
        return random.choice(responses)
    else:
        return "I'm sorry, I don't have an answer for that."

# Function to predict intent and confidence
def predict_intent(user_input):
    processed_input = preprocess_input(user_input)
    probabilities = mlp_model.predict_proba(processed_input)[0]
    prediction = mlp_model.classes_[probabilities.argmax()]
    confidence = probabilities.max()
    return prediction, confidence

app = Flask(__name__)

@app.route("/")
def index():
    print("Index route accessed")
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    prediction, confidence = predict_intent(msg)
    
    if confidence < 0.6:
        response = "I'm not very confident about this. Can you please provide more details?"
    else:
        response = generate_response(prediction)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
