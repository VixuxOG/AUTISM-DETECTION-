import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from flask import Flask, request, jsonify

class AutismDetectionModel:
    def __init__(self):
        # Define parameter groups and their weights
        self.parameter_groups = {
            'social_communication': {
                'name_response': 0.08, 'eye_contact': 0.08, 'pointing_interest': 0.07, 'pointing_request': 0.07,
                'follow_look': 0.06, 'simple_gestures': 0.06, 'check_reaction': 0.06, 'comfort_others': 0.05
            },
            'speech_and_language': {
                'speech_clarity': 0.07, 'word_count': 0.06, 'first_words': 0.06, 'echo_speech': 0.05, 'pretend_play': 0.05
            },
            'repetitive_behaviors': {
                'line_objects': 0.04, 'spinning_interest': 0.04, 'repetitive_actions': 0.04,
                'repetitive_twiddling': 0.03, 'object_interest': 0.03
            },
            'sensory_patterns': {
                'unusual_sensory': 0.03, 'noise_sensitivity': 0.03, 'unusual_finger_movements': 0.03,
                'tiptoe_walking': 0.02, 'staring': 0.02, 'hand_placing': 0.02, 'routine_adaptation': 0.02
            }
        }
        
        # Initialize models
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=5, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42),
            'neural_network': MLPClassifier(hidden_layer_sizes=(64, 32, 16), activation='relu', max_iter=1000, random_state=42)
        }
        self.scaler = StandardScaler()
        
    def preprocess_answers(self, answers):
        """Convert survey answers to feature vector"""
        features = []
        for group in self.parameter_groups.values():
            for question in group:
                score = answers.get(question, 0) * group[question]
                features.append(score)
        return np.array(features).reshape(1, -1)
        
    def calculate_risk_score(self, answers):
        """Calculate risk score and confidence level"""
        features = self.preprocess_answers(answers)
        scaled_features = self.scaler.transform(features)
        final_probability = np.mean([model.predict_proba(scaled_features)[0, 1] for model in self.models.values()])
        risk_level = 'High Risk' if final_probability > 0.6 else 'Medium Risk' if final_probability > 0.3 else 'Low Risk'
        return {'risk_level': risk_level, 'risk_score': round(final_probability, 3)}
        
app = Flask(__name__)
model = AutismDetectionModel()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    answers = data.get('answers', {})
    results = model.calculate_risk_score(answers)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
