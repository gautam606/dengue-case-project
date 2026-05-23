"""
Flask Web Application - AI-Powered Dengue Prediction & Detection System
Main application file with routes and AI prediction logic
"""

from flask import Flask, render_template, request, jsonify, redirect
import joblib
import numpy as np
import pandas as pd
from database import DengueDatabase
import os
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dengue-ai-system-2024-secure-key'

# Initialize database
db = DengueDatabase()

# Global variable for models
models = {}

def load_ai_models():
    global models
    models_dir = '../models'
    try:
        print("\n[LOADING] AI Models...")
        models['outbreak_lr'] = joblib.load(f'{models_dir}/outbreak_lr_model.pkl')
        models['outbreak_rf'] = joblib.load(f'{models_dir}/outbreak_rf_model.pkl')
        models['outbreak_scaler'] = joblib.load(f'{models_dir}/outbreak_scaler.pkl')
        print("[OK] Outbreak prediction models loaded")
        models['detection_lr'] = joblib.load(f'{models_dir}/detection_lr_model.pkl')
        models['detection_rf'] = joblib.load(f'{models_dir}/detection_rf_model.pkl')
        models['detection_svm'] = joblib.load(f'{models_dir}/detection_svm_model.pkl')
        models['detection_scaler'] = joblib.load(f'{models_dir}/detection_scaler.pkl')
        print("[OK] Detection models loaded")
        print("[SUCCESS] All AI models loaded successfully!\n")
        return True
    except Exception as e:
        print(f"\n[ERROR] Failed to load models: {e}")
        print("[INFO] Please run 'python train_models.py' first to train the models.\n")
        return False

models_loaded = load_ai_models()

# ==========================================
# WEB PAGE ROUTES
# ==========================================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/outbreak')
def outbreak_page():
    return render_template('outbreak.html')

@app.route('/detection')
def detection_page():
    return render_template('detection.html')

@app.route('/patient')
def patient_redirect():
    return redirect('/detection')

@app.route('/fever-monitor')
def fever_monitor_page():
    history = db.get_fever_history(limit=50)
    return render_template('fever_monitor.html', fever_history=history)

@app.route('/emergency')
def emergency_page():
    return render_template('emergency.html')

@app.route('/dashboard')
def dashboard():
    stats = db.get_dashboard_statistics()
    return render_template('dashboard.html', stats=stats)

# ==========================================
# OUTBREAK PREDICTION API (UNCHANGED)
# ==========================================

@app.route('/api/predict/outbreak', methods=['POST'])
def predict_outbreak():
    if not models_loaded:
        return jsonify({'error': 'AI models not loaded.', 'success': False}), 500
    try:
        data = request.get_json()
        temperature = float(data['temperature'])
        rainfall = float(data['rainfall'])
        humidity = float(data['humidity'])
        population_density = float(data['population_density'])
        model_type = data.get('model', 'rf')

        features = np.array([[temperature, rainfall, humidity, population_density]])
        features_scaled = models['outbreak_scaler'].transform(features)

        if model_type == 'lr':
            model = models['outbreak_lr']
            model_name = 'Logistic Regression'
        else:
            model = models['outbreak_rf']
            model_name = 'Random Forest AI'

        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        risk_levels = ['Low', 'Medium', 'High']
        risk_level = risk_levels[prediction]

        explanation = generate_outbreak_explanation(temperature, rainfall, humidity, risk_level)
        input_data = {'temperature': temperature, 'rainfall': rainfall, 'humidity': humidity,
                      'population_density': population_density}
        prediction_result = {'risk_level': risk_level, 'risk_code': int(prediction),
                             'probabilities': {'low': float(probabilities[0]), 'medium': float(probabilities[1]), 'high': float(probabilities[2])}}

        db.save_environmental_data(input_data.copy())
        db.save_prediction('outbreak', input_data, prediction_result, model_name, explanation)

        return jsonify({
            'success': True, 'risk_level': risk_level, 'risk_code': int(prediction),
            'probabilities': prediction_result['probabilities'],
            'confidence': float(max(probabilities)) * 100,
            'model_used': model_name, 'explanation': explanation,
            'recommendations': get_outbreak_recommendations(risk_level)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

# ==========================================
# DETECTION API (NEW - 13 FEATURES, 3 RISK LEVELS)
# ==========================================

DETECTION_FEATURES = [
    'high_fever', 'fever_duration_days', 'biphasic_fever',
    'muscle_joint_pain', 'pain_behind_eyes', 'headache',
    'fatigue', 'vomiting', 'skin_rash',
    'bleeding_signs', 'severe_abdominal_pain', 'rapid_breathing', 'extreme_fatigue_restlessness'
]

@app.route('/api/predict/detection', methods=['POST'])
def predict_detection():
    if not models_loaded:
        return jsonify({'error': 'AI models not loaded.', 'success': False}), 500
    try:
        data = request.get_json()
        feature_values = [float(data[f]) for f in DETECTION_FEATURES]
        model_type = data.get('model', 'rf')

        features = np.array([feature_values])
        features_scaled = models['detection_scaler'].transform(features)

        if model_type == 'lr':
            model, model_name = models['detection_lr'], 'Logistic Regression'
        elif model_type == 'svm':
            model, model_name = models['detection_svm'], 'Support Vector Machine AI'
        else:
            model, model_name = models['detection_rf'], 'Random Forest AI'

        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        risk_levels = ['Low', 'Moderate', 'High']
        risk_level = risk_levels[prediction]

        explanation = generate_detection_explanation(data, risk_level)
        input_data = {f: float(data[f]) for f in DETECTION_FEATURES}
        prediction_result = {
            'risk_level': risk_level, 'risk_code': int(prediction),
            'probabilities': {'low': float(probabilities[0]), 'moderate': float(probabilities[1]), 'high': float(probabilities[2])}
        }

        db.save_symptom_data(input_data.copy())
        db.save_prediction('detection', input_data, prediction_result, model_name, explanation)

        return jsonify({
            'success': True, 'risk_level': risk_level, 'risk_code': int(prediction),
            'probabilities': prediction_result['probabilities'],
            'confidence': float(max(probabilities)) * 100,
            'model_used': model_name, 'explanation': explanation,
            'recommendations': get_detection_recommendations(risk_level)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

# ==========================================
# FEVER MONITORING API
# ==========================================

@app.route('/api/fever/log', methods=['POST'])
def log_fever():
    try:
        data = request.get_json()
        fever_data = {
            'temperature': float(data['temperature']),
            'reading_time': data.get('reading_time', ''),
            'notes': data.get('notes', '')
        }
        db.save_fever_reading(fever_data)
        return jsonify({'success': True, 'message': 'Fever reading logged.'})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

@app.route('/api/fever/history', methods=['GET'])
def get_fever_history():
    history = db.get_fever_history(limit=50)
    # Convert datetime objects to strings
    for h in history:
        if 'timestamp' in h:
            h['timestamp'] = h['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'success': True, 'history': history})

# ==========================================
# SYMPTOM CHATBOT API
# ==========================================

@app.route('/api/symptom-chat', methods=['POST'])
def symptom_chat():
    try:
        data = request.get_json()
        message = data.get('message', '').lower().strip()
        response = get_chatbot_response(message)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

def get_chatbot_response(message):
    """Rule-based symptom assessment chatbot."""
    if any(w in message for w in ['hello', 'hi', 'hey', 'start']):
        return ("👋 Hello! I'm the Dengue Symptom Assistant. I can help you understand dengue symptoms.\n\n"
                "You can ask me about:\n• Fever patterns\n• Physical symptoms\n• Warning signs\n• Medication safety\n• When to see a doctor\n\n"
                "⚠️ I am NOT a doctor. Always consult a medical professional.")
    if any(w in message for w in ['fever', 'temperature', 'hot']):
        return ("🌡️ **Dengue Fever Patterns:**\n\n"
                "• High fever (39-40°C / 102-104°F) lasting 2-7 days\n"
                "• **Saddleback Fever**: Fever drops temporarily then returns\n"
                "• Usually appears 4-10 days after mosquito bite\n\n"
                "👉 Use our **Fever Monitor** to track your temperature over time.\n"
                "⚠️ If fever persists >3 days, consult a doctor immediately.")
    if any(w in message for w in ['pain', 'muscle', 'joint', 'body', 'eye', 'headache', 'breakbone']):
        return ("💪 **Dengue Pain Symptoms:**\n\n"
                "• Severe muscle & joint pain (\"Breakbone Fever\")\n"
                "• Intense pain behind the eyes (retro-orbital pain)\n"
                "• Severe headache, especially frontal\n\n"
                "These are hallmark dengue symptoms. Use **Dengue Detection** for AI assessment.")
    if any(w in message for w in ['warning', 'danger', 'emergency', 'bleed', 'blood', 'severe']):
        return ("🚨 **Dengue Warning Signs (SEEK IMMEDIATE MEDICAL HELP):**\n\n"
                "• Bleeding from gums or nose\n• Blood in vomit or urine\n"
                "• Severe abdominal pain\n• Rapid breathing\n"
                "• Extreme fatigue or restlessness\n\n"
                "👉 Visit our **Emergency Warning** page for more details.\n"
                "🏥 **Go to the hospital immediately if you have these signs!**")
    if any(w in message for w in ['medicine', 'medication', 'drug', 'aspirin', 'paracetamol', 'ibuprofen']):
        return ("💊 **Medication Safety for Dengue:**\n\n"
                "✅ **SAFE**: Paracetamol (Acetaminophen) for fever/pain\n"
                "❌ **AVOID**: Aspirin - increases bleeding risk\n"
                "❌ **AVOID**: Ibuprofen/NSAIDs - increases bleeding risk\n\n"
                "⚠️ Always follow your doctor's prescription.")
    if any(w in message for w in ['tourniquet', 'petechiae', 'red dot', 'red spot']):
        return ("🔴 **Tourniquet Test:**\n\n"
                "• A clinical test where a blood pressure cuff is inflated\n"
                "• After 5 minutes, small red dots (petechiae) may appear\n"
                "• More than 20 petechiae per square inch suggests dengue\n\n"
                "⚠️ This is only a clinical indicator, NOT a definitive diagnosis.\n"
                "Only a trained medical professional should perform this test.")
    if any(w in message for w in ['rash', 'skin']):
        return ("🔴 **Dengue Skin Rash:**\n\n"
                "• Appears 2-5 days after fever onset\n"
                "• Flat red rash (maculopapular) on the body\n"
                "• May be itchy\n• Usually spreads from trunk to limbs\n\n"
                "If you notice a rash with fever, use our **Detection** page for assessment.")
    if any(w in message for w in ['prevent', 'mosquito', 'protect']):
        return ("🦟 **Dengue Prevention:**\n\n"
                "• Use mosquito repellent\n• Wear long sleeves and pants\n"
                "• Remove standing water around your home\n"
                "• Use mosquito nets while sleeping\n• Keep windows/doors screened\n\n"
                "Prevention is the best protection against dengue!")
    return ("🤖 I can help with dengue-related questions. Try asking about:\n\n"
            "• \"What are dengue fever patterns?\"\n• \"What are warning signs?\"\n"
            "• \"What medication is safe?\"\n• \"Tell me about the tourniquet test\"\n"
            "• \"How to prevent dengue?\"\n\n"
            "⚠️ This is for educational purposes only. Always consult a doctor.")

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    stats = db.get_dashboard_statistics()
    return jsonify(stats)

# ==========================================
# EXPLANATION FUNCTIONS
# ==========================================

def generate_outbreak_explanation(temp, rainfall, humidity, risk_level):
    explanation = {'factors': [], 'summary': ''}
    if temp > 28:
        explanation['factors'].append({'factor': 'Temperature', 'value': f'{temp}°C', 'status': 'risk', 'reason': 'Optimal for mosquito breeding (>28°C)'})
    else:
        explanation['factors'].append({'factor': 'Temperature', 'value': f'{temp}°C', 'status': 'safe', 'reason': 'Below optimal mosquito breeding temperature'})
    if rainfall > 150:
        explanation['factors'].append({'factor': 'Rainfall', 'value': f'{rainfall}mm', 'status': 'risk', 'reason': 'Creates standing water for mosquito breeding'})
    else:
        explanation['factors'].append({'factor': 'Rainfall', 'value': f'{rainfall}mm', 'status': 'safe', 'reason': 'Insufficient for extensive breeding sites'})
    if humidity > 70:
        explanation['factors'].append({'factor': 'Humidity', 'value': f'{humidity}%', 'status': 'risk', 'reason': 'High humidity increases mosquito survival'})
    else:
        explanation['factors'].append({'factor': 'Humidity', 'value': f'{humidity}%', 'status': 'safe', 'reason': 'Humidity within safe range'})
    risk_count = sum(1 for f in explanation['factors'] if f['status'] == 'risk')
    if risk_level == 'High':
        explanation['summary'] = f"AI detected {risk_count}/3 high-risk environmental factors. Conditions are highly favorable for dengue outbreak."
    elif risk_level == 'Medium':
        explanation['summary'] = f"AI detected {risk_count}/3 risk factors. Moderate conditions for dengue transmission."
    else:
        explanation['summary'] = f"AI detected {risk_count}/3 risk factors. Low probability of dengue outbreak."
    return explanation

def generate_detection_explanation(data, risk_level):
    explanation = {'factors': [], 'summary': ''}
    # Fever group
    if int(data.get('high_fever', 0)):
        explanation['factors'].append({'factor': 'High Fever', 'value': 'Present', 'status': 'symptom', 'reason': 'Primary indicator of dengue infection', 'group': 'fever'})
    dur = int(data.get('fever_duration_days', 0))
    if dur >= 3:
        explanation['factors'].append({'factor': 'Fever Duration', 'value': f'{dur} days', 'status': 'symptom', 'reason': 'Prolonged fever (≥3 days) is concerning', 'group': 'fever'})
    if int(data.get('biphasic_fever', 0)):
        explanation['factors'].append({'factor': 'Biphasic Fever', 'value': 'Detected', 'status': 'symptom', 'reason': 'Saddleback pattern is characteristic of dengue', 'group': 'fever'})
    # Physical group
    symptom_map = {
        'muscle_joint_pain': ('Muscle/Joint Pain', 'Breakbone fever — hallmark dengue symptom'),
        'pain_behind_eyes': ('Pain Behind Eyes', 'Retro-orbital pain common in dengue'),
        'headache': ('Headache', 'Common dengue symptom'),
        'fatigue': ('Fatigue', 'General weakness associated with infection'),
        'vomiting': ('Vomiting', 'Gastrointestinal involvement'),
        'skin_rash': ('Skin Rash', 'Maculopapular rash typical of dengue')
    }
    for key, (label, reason) in symptom_map.items():
        if int(data.get(key, 0)):
            explanation['factors'].append({'factor': label, 'value': 'Present', 'status': 'symptom', 'reason': reason, 'group': 'physical'})
    # Warning signs group
    warning_map = {
        'bleeding_signs': ('Bleeding Signs', '⚠️ Hemorrhagic indicator — seek immediate care'),
        'severe_abdominal_pain': ('Severe Abdominal Pain', '⚠️ Warning sign of severe dengue'),
        'rapid_breathing': ('Rapid Breathing', '⚠️ Respiratory distress indicator'),
        'extreme_fatigue_restlessness': ('Extreme Fatigue/Restlessness', '⚠️ Sign of worsening condition')
    }
    for key, (label, reason) in warning_map.items():
        if int(data.get(key, 0)):
            explanation['factors'].append({'factor': label, 'value': 'Present', 'status': 'warning', 'reason': reason, 'group': 'warning'})

    symptom_count = len(explanation['factors'])
    warning_count = sum(1 for f in explanation['factors'] if f['status'] == 'warning')
    if risk_level == 'High':
        explanation['summary'] = f"AI detected {symptom_count} symptoms/signs including {warning_count} warning sign(s). HIGH risk of dengue — seek medical attention immediately."
    elif risk_level == 'Moderate':
        explanation['summary'] = f"AI detected {symptom_count} symptoms. MODERATE dengue risk — monitor closely and consult a doctor if symptoms worsen."
    else:
        explanation['summary'] = f"AI detected {symptom_count} symptom(s). LOW dengue risk — continue monitoring and maintain hydration."
    return explanation

# ==========================================
# RECOMMENDATION FUNCTIONS
# ==========================================

def get_outbreak_recommendations(risk_level):
    recs = {
        'Low': ['Continue routine environmental monitoring', 'Maintain current sanitation standards',
                'Regular community awareness programs', 'Monitor weather patterns'],
        'Medium': ['Increase mosquito surveillance', 'Intensify community awareness campaigns',
                   'Implement targeted mosquito control', 'Monitor vulnerable populations', 'Prepare healthcare facilities'],
        'High': ['URGENT: Alert health authorities immediately', 'Intensive mosquito control operations',
                 'Mass public health campaigns', 'Community-wide cleanup drives',
                 'Activate emergency response protocols', 'Consider preventive treatment programs']
    }
    return recs.get(risk_level, [])

def get_detection_recommendations(risk_level):
    if risk_level == 'High':
        return [
            '🚨 SEEK IMMEDIATE MEDICAL ATTENTION',
            'Visit the nearest hospital or emergency room',
            'Request Complete Blood Count (CBC) and NS1 antigen test',
            'Stay hydrated — drink ORS, water, coconut water',
            '💊 Take only Paracetamol for fever (avoid Aspirin & Ibuprofen)',
            'Watch for warning signs: bleeding, severe abdominal pain',
            'Complete bed rest is essential',
            'Monitor temperature every 4-6 hours'
        ]
    elif risk_level == 'Moderate':
        return [
            '⚠️ Consult a doctor within 24 hours',
            'Get a blood test (CBC) to check platelet count',
            'Drink plenty of fluids (3-4 liters/day)',
            '💊 Use only Paracetamol for fever — AVOID Aspirin & Ibuprofen',
            'Rest and monitor symptoms closely',
            'Return to hospital if warning signs appear',
            'Track your fever pattern using the Fever Monitor'
        ]
    else:
        return [
            '✅ Continue monitoring your symptoms',
            'Maintain good hydration',
            'If fever develops or persists, consult a doctor',
            'Practice mosquito prevention measures',
            'Use mosquito repellent and nets',
            '💊 If needed, take only Paracetamol — avoid NSAIDs'
        ]

# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ==========================================
# APPLICATION STARTUP
# ==========================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("AI-POWERED DENGUE PREDICTION AND DETECTION SYSTEM")
    print("="*70)
    if models_loaded:
        print("\n[STATUS] All systems operational")
        print("[AI] Models loaded and ready")
        print(f"[DATABASE] {'Connected' if db.connected else 'Not connected (data will not persist)'}")
        print("\n[ACCESS] Web application at: http://127.0.0.1:5000")
        print("[INFO] Press CTRL+C to stop the server")
        print("="*70 + "\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n[ERROR] Cannot start application - models not loaded")
        print("[ACTION] Please run: python train_models.py")
        print("="*70 + "\n")
        sys.exit(1)
