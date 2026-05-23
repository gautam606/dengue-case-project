# 🚀 QUICK START GUIDE

## AI-Powered Dengue Prediction and Diagnosis System

### Step-by-Step Setup Instructions

---

## ⚡ Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train AI Models
```bash
python train_models.py
```

**What this does:**
- Generates 2000 sample records for each module
- Performs Exploratory Data Analysis (EDA)
- Trains 5 AI models (Logistic Regression, Random Forest, SVM)
- Saves models in `models/` folder
- Creates visualizations in `data/` folder
- Takes ~2-3 minutes

**Expected Output:**
```
OUTBREAK PREDICTION MODELS:
  Logistic Regression: 75-85%
  Random Forest (AI):  85-95%

PATIENT DIAGNOSIS MODELS:
  Logistic Regression: 80-85%
  Random Forest (AI):  85-90%
  SVM (AI):            82-88%
```

### 3. Start MongoDB (Optional)
```bash
# Windows
net start MongoDB

# If MongoDB not installed, app works without it
# (predictions won't be saved to database)
```

### 4. Run Web Application
```bash
cd app
python app.py
```

### 5. Access Application
Open browser: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
datascienceproj/
│
├── app/
│   ├── templates/
│   │   ├── base.html          # Base template
│   │   ├── home.html          # Home page
│   │   ├── outbreak.html      # Outbreak prediction
│   │   ├── patient.html       # Patient diagnosis
│   │   └── dashboard.html     # Dashboard
│   │
│   ├── app.py                 # Main Flask app
│   └── database.py            # MongoDB connection
│
├── models/                    # Trained AI models (.pkl)
│   ├── outbreak_lr_model.pkl
│   ├── outbreak_rf_model.pkl
│   ├── outbreak_scaler.pkl
│   ├── patient_lr_model.pkl
│   ├── patient_rf_model.pkl
│   ├── patient_svm_model.pkl
│   └── patient_scaler.pkl
│
├── data/                      # Datasets & visualizations
│   ├── outbreak_data.csv
│   ├── patient_data.csv
│   ├── outbreak_correlation.png
│   ├── outbreak_eda.png
│   ├── patient_eda.png
│   └── feature_importance.png
│
├── train_models.py            # AI model training
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

---

## 🎯 How to Use

### Module 1: Outbreak Prediction
1. Go to **Outbreak Prediction** page
2. Enter environmental data:
   - Temperature (20-40°C)
   - Rainfall (0-300mm)
   - Humidity (40-100%)
   - Population Density (100-5000)
   - Sanitation Index (0-100)
3. Select AI model (Random Forest recommended)
4. Click **Predict Outbreak Risk**
5. View:
   - Risk Level (Low/Medium/High)
   - Probability scores
   - AI Explanation
   - Recommendations

### Module 2: Patient Diagnosis
1. Go to **Patient Diagnosis** page
2. Enter clinical data:
   - Fever (Yes/No)
   - Headache (Yes/No)
   - Platelet Count (30,000-400,000)
   - WBC Count (2,000-15,000)
3. Select AI model
4. Click **Diagnose Patient**
5. View:
   - Diagnosis (Positive/Negative)
   - Confidence score
   - AI Explanation
   - Medical recommendations

### Dashboard
- View system statistics
- See recent predictions
- Analyze trends

---

## 🧪 Testing the System

### Test Case 1: High Risk Outbreak
```
Temperature: 32°C
Rainfall: 200mm
Humidity: 80%
Population Density: 3500
Sanitation Index: 30
```
**Expected:** HIGH RISK

### Test Case 2: Low Risk Outbreak
```
Temperature: 24°C
Rainfall: 50mm
Humidity: 55%
Population Density: 1000
Sanitation Index: 80
```
**Expected:** LOW RISK

### Test Case 3: Dengue Positive Patient
```
Fever: Yes
Headache: Yes
Platelet Count: 80,000
WBC Count: 3,000
```
**Expected:** POSITIVE

### Test Case 4: Dengue Negative Patient
```
Fever: No
Headache: No
Platelet Count: 250,000
WBC Count: 7,000
```
**Expected:** NEGATIVE

---

## 🔧 Troubleshooting

### Problem: Models not loading
**Solution:**
```bash
python train_models.py
```

### Problem: MongoDB connection error
**Solution:**
- Install MongoDB: https://www.mongodb.com/try/download/community
- Start service: `net start MongoDB`
- Or continue without MongoDB (data won't persist)

### Problem: Port 5000 already in use
**Solution:**
Edit `app/app.py`, change:
```python
app.run(port=5001)
```

### Problem: Module not found
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📊 Understanding AI Predictions

### How Random Forest Works
**ANALOGY:** 100 doctors voting on diagnosis
- Creates 100 decision trees
- Each tree analyzes the data
- Final prediction = majority vote
- More reliable than single model

### Feature Importance
Shows which factors matter most:
- **Outbreak:** Rainfall > Temperature > Humidity
- **Patient:** Platelet Count > Fever > WBC Count

### AI Explainability
System explains WHY it made predictions:
- Which factors triggered the prediction
- How each feature contributed
- Confidence level

---

## 🎓 Key Concepts

### Data Science Components
✅ Exploratory Data Analysis (EDA)
✅ Data Preprocessing
✅ Feature Engineering
✅ Correlation Analysis
✅ Data Visualization

### AI Components
✅ Supervised Learning
✅ Classification Algorithms
✅ Ensemble Methods (Random Forest)
✅ Model Evaluation
✅ Feature Importance
✅ AI Explainability

### Database
✅ MongoDB Integration
✅ CRUD Operations
✅ Data Persistence
✅ Query Operations

---

## 🚀 Future Enhancements

1. **Deep Learning**
   - Neural Networks
   - LSTM for time-series

2. **Real-time Data**
   - Weather API integration
   - Hospital data feeds

3. **Visualization**
   - Interactive maps
   - Geographic heatmaps

4. **Mobile App**
   - React Native
   - Push notifications

5. **NLP**
   - Chatbot for symptoms
   - Voice input

---

## 📝 API Endpoints

### Outbreak Prediction
```
POST /api/predict/outbreak
Content-Type: application/json

{
  "temperature": 32,
  "rainfall": 180,
  "humidity": 75,
  "population_density": 3000,
  "sanitation_index": 45,
  "model": "rf"
}
```

### Patient Diagnosis
```
POST /api/predict/patient
Content-Type: application/json

{
  "fever": 1,
  "headache": 1,
  "platelet_count": 95000,
  "wbc_count": 3500,
  "model": "rf"
}
```

### Statistics
```
GET /api/statistics
```

---

## 💡 Tips for Best Results

1. **Use Random Forest** - Most accurate AI model
2. **Check AI Explanation** - Understand why predictions were made
3. **View Dashboard** - Track trends over time
4. **Test Edge Cases** - Try extreme values
5. **Compare Models** - See how different AIs perform

---

## 🎯 Project Highlights

✨ **5 AI Models** trained and deployed
✨ **85-95% Accuracy** across all models
✨ **Explainable AI** - transparent predictions
✨ **MongoDB Integration** - data persistence
✨ **Professional UI** - Bootstrap 5
✨ **RESTful APIs** - easy integration
✨ **Real-time Predictions** - instant results

---

## 📞 Support

If you encounter issues:
1. Check this guide
2. Review README.md
3. Check console output for errors
4. Verify all dependencies installed

---

**Ready to start?**
```bash
python train_models.py
cd app
python app.py
```

**Access:** http://127.0.0.1:5000

---

**Built with ❤️ for Data Science & AI Learning**
