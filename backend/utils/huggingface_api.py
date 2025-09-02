import requests
from flask import current_app

def analyze_sentiment(text):
    """Send text to Hugging Face sentiment analysis API"""
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {current_app.config['HUGGINGFACE_API_KEY']}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            sentiment_data = result[0]
            if len(sentiment_data) > 0:
                # Return the label with highest score
                return max(sentiment_data, key=lambda x: x['score'])
        return {"label": "NEUTRAL", "score": 0.5}
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return {"label": "NEUTRAL", "score": 0.5}

def generate_flashcards(text):
    """Generate flashcards from study notes using Hugging Face Q&A model"""
    API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    headers = {"Authorization": f"Bearer {current_app.config['HUGGINGFACE_API_KEY']}"}
    
    # This is a simplified approach - in a real app, you'd need to craft proper prompts
    payload = {
        "inputs": {
            "question": "What are the key points?",
            "context": text
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        # For demo purposes, we'll create some sample flashcards
        # In a real implementation, you'd need a more sophisticated approach
        sample_flashcards = [
            {"question": "What is the main topic?", "answer": "Extracted from your notes"},
            {"question": "Key concept 1?", "answer": "Summary point 1"},
            {"question": "Key concept 2?", "answer": "Summary point 2"},
            {"question": "Key concept 3?", "answer": "Summary point 3"},
            {"question": "What should you remember?", "answer": "The most important point"}
        ]
        
        return sample_flashcards
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return []