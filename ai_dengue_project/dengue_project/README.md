# AI-Powered Dengue Prediction and Diagnosis System

## 🎯 Project Overview

An intelligent web-based system that combines **Data Science** and **Artificial Intelligence** to:
1. **Predict dengue outbreak risk** using environmental data
2. **Diagnose dengue infection** using clinical patient data

## 🏗️ Project Structure

```
datascienceproj/
│
├── app/
│   ├── templates/          # HTML templates
│   ├── static/            # CSS, JS, images
│   ├── app.py             # Main Flask application
│   ├── database.py        # MongoDB connection
│   └── ml_models.py       # Model loading and prediction
│
├── models/                # Saved ML models (.pkl files)
├── data/                  # Datasets
├── notebooks/             # Jupyter notebooks for EDA
│
├── train_models.py        # Model training script
├── eda_analysis.py        # Exploratory Data Analysis
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🚀 Quick Start Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start MongoDB (Optional)
```bash
# Windows
net start MongoDB

# The system works without MongoDB but won't store data
```

### Step 3: Train AI Models
```bash
python train_models.py
```
This will:
- Create sample datasets
- Train 5 AI models
- Save models in `models/` folder
- Display accuracy metrics

### Step 4: Run Web Application
```bash
cd app
python app.py
```

Access at: **http://127.0.0.1:5000**

## 📊 Modules

### Module 1: Outbreak Prediction (Environmental AI)
**Input Features:**
- Temperature (°C)
- Rainfall (mm)
- Humidity (%)
- Population Density (per km²)
- Sanitation Index (0-100)

**AI Models:**
- Logistic Regression (Baseline)
- Random Forest (Advanced AI)

**Output:**
- Risk Level: Low / Medium / High
- Probability scores
- AI Explanation

### Module 2: Patient Diagnosis (Clinical AI)
**Input Features:**
- Fever (Yes/No)
- Headache (Yes/No)
- Platelet Count
- WBC Count

**AI Models:**
- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)

**Output:**
- Diagnosis: Positive / Negative
- Confidence score
- Medical recommendations

## 🧠 AI & Data Science Components

### Data Science
✅ Exploratory Data Analysis (EDA)
✅ Data Cleaning & Preprocessing
✅ Feature Engineering
✅ Correlation Analysis
✅ Data Visualization
✅ Statistical Analysis

### Artificial Intelligence
✅ Predictive Modeling
✅ Classification Algorithms
✅ Feature Importance Analysis
✅ Model Comparison
✅ AI Explainability (Why predictions were made)
✅ Ensemble Learning (Random Forest)

### Database Management
✅ MongoDB Integration
✅ Data Storage & Retrieval
✅ Prediction History
✅ Real-time Statistics

## 📈 Model Performance

### Outbreak Prediction Models
- Logistic Regression: ~75-85% accuracy
- Random Forest: ~85-95% accuracy

### Patient Diagnosis Models
- Logistic Regression: ~80-85% accuracy
- Random Forest: ~85-90% accuracy
- SVM: ~82-88% accuracy

## 🎨 Web Application Features

### Pages
1. **Home** - System overview
2. **Outbreak Prediction** - Environmental data input
3. **Patient Diagnosis** - Clinical data input
4. **Dashboard** - Statistics and visualizations

### Features
- Interactive forms
- Real-time predictions
- Visual results
- AI explanations
- Historical data
- Performance metrics

## 🗄️ MongoDB Setup

### Database Structure
```
dengue_system/
├── environmental_data     # Outbreak prediction inputs
├── patient_data          # Patient diagnosis inputs
└── predictions           # All prediction results
```

### Connection
```python
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['dengue_system']
```

## 📊 Visualizations

The system generates:
- Correlation heatmaps
- Feature importance charts
- Risk distribution graphs
- Confusion matrices
- Trend analysis plots

## 🔬 How AI Works (Simple Explanation)

### Outbreak Prediction AI
**Think of it like a weather forecaster:**
- Looks at temperature, rain, humidity
- Learns patterns from past outbreaks
- Predicts if conditions are right for dengue

**Random Forest = 100 experts voting**
- Creates 100 decision trees
- Each tree gives an opinion
- Final prediction = majority vote

### Patient Diagnosis AI
**Think of it like an experienced doctor:**
- Checks symptoms (fever, headache)
- Examines lab results (platelets, WBC)
- Compares with thousands of past cases
- Makes diagnosis based on patterns

## 🎯 AI Explainability

The system explains WHY it made predictions:

**Example: "High Risk" Prediction**
```
Reasons:
✓ Temperature > 28°C (Mosquito breeding optimal)
✓ Rainfall > 150mm (Standing water)
✓ Humidity > 70% (Mosquito survival)
✗ Sanitation Index < 50 (Poor hygiene)

Conclusion: 4/5 risk factors present → HIGH RISK
```

## 🚀 Future Improvements

### AI Enhancements
1. **Deep Learning Models**
   - Neural Networks for complex patterns
   - LSTM for time-series prediction

2. **Real-time Data Integration**
   - Weather API integration
   - Hospital data feeds

3. **Advanced Visualization**
   - Interactive maps (Folium/Leaflet)
   - Geographic risk zones
   - Heatmaps of outbreak areas

4. **Mobile Application**
   - React Native app
   - Push notifications for high-risk alerts

5. **Natural Language Processing**
   - Chatbot for symptom checking
   - Voice-based input

## 🛠️ Technologies Used

| Category | Technologies |
|----------|-------------|
| **Backend** | Flask, Python |
| **Frontend** | HTML, CSS, Bootstrap, JavaScript |
| **AI/ML** | scikit-learn, Random Forest, SVM |
| **Database** | MongoDB, pymongo |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Data Science** | Pandas, NumPy |

## 📝 Key Concepts Explained

### 1. Feature Engineering
**Analogy:** Like a chef preparing ingredients before cooking
- Raw data = raw vegetables
- Feature engineering = chopping, seasoning
- Better preparation = better results

### 2. Model Training
**Analogy:** Teaching a student with examples
- Show 1000 examples of dengue cases
- Student (model) learns patterns
- Test with new cases to check learning

### 3. Ensemble Learning (Random Forest)
**Analogy:** Asking multiple doctors for diagnosis
- 100 doctors (trees) examine patient
- Each gives opinion
- Final diagnosis = majority vote
- More reliable than single opinion

### 4. Feature Importance
**Analogy:** Finding the most important clues
- Which symptom matters most?
- Temperature or rainfall - which predicts better?
- Helps focus on critical factors

### 5. Confusion Matrix
**Analogy:** Report card for AI
- True Positive: Correctly identified dengue
- False Positive: False alarm
- True Negative: Correctly ruled out dengue
- False Negative: Missed dengue case

## 🎓 Learning Outcomes

After completing this project, you'll understand:
- End-to-end Data Science pipeline
- AI model development and deployment
- Database integration
- Web application development
- Model evaluation and interpretation
- Real-world AI application

## 📞 Troubleshooting

### Models not loading?
```bash
python train_models.py
```

### MongoDB connection error?
System works without MongoDB, but data won't persist.
Install MongoDB from: https://www.mongodb.com/try/download/community

### Port 5000 already in use?
Change port in `app.py`:
```python
app.run(port=5001)
```

## 🌟 Project Highlights

✨ **Data Science:** Complete EDA, preprocessing, visualization
✨ **AI/ML:** Multiple algorithms, ensemble methods
✨ **Database:** MongoDB integration for data persistence
✨ **Web App:** Professional Flask application
✨ **Explainability:** AI reasoning for predictions
✨ **Scalability:** Modular design for easy expansion

## 📄 License

Educational project - Free to use and modify

---

**Built with ❤️ for Data Science & AI Learning**
