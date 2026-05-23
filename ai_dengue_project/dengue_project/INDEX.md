# 📋 PROJECT INDEX

## AI-Powered Dengue Prediction and Diagnosis System
### Complete File List and Description

---

## 🚀 QUICK START

**Option 1: Automated (Windows)**
```bash
run.bat
```

**Option 2: Manual**
```bash
pip install -r requirements.txt
python train_models.py
cd app
python app.py
```

**Access:** http://127.0.0.1:5000

---

## 📁 COMPLETE FILE STRUCTURE

### 📄 Root Files

| File | Description | Lines | Purpose |
|------|-------------|-------|---------|
| `README.md` | Complete documentation | 400+ | Project overview, setup, features |
| `QUICKSTART.md` | Quick setup guide | 300+ | Step-by-step instructions |
| `PROJECT_SUMMARY.md` | Detailed summary | 500+ | Technical details, API docs |
| `INDEX.md` | This file | 200+ | File navigation |
| `requirements.txt` | Dependencies | 10 | Python packages |
| `train_models.py` | Model training | 600+ | AI training pipeline |
| `run.bat` | Auto-run script | 15 | Windows automation |

### 📂 app/ - Web Application

| File | Description | Lines | Purpose |
|------|-------------|-------|---------|
| `app.py` | Main Flask app | 500+ | Web server, routes, APIs |
| `database.py` | MongoDB module | 300+ | Database operations |

### 📂 app/templates/ - HTML Pages

| File | Description | Lines | Purpose |
|------|-------------|-------|---------|
| `base.html` | Base template | 200+ | Common layout, navigation |
| `home.html` | Landing page | 250+ | System overview |
| `outbreak.html` | Outbreak prediction | 300+ | Environmental data input |
| `patient.html` | Patient diagnosis | 350+ | Clinical data input |
| `dashboard.html` | Statistics | 250+ | Charts and metrics |
| `404.html` | Error page | 30 | Page not found |
| `500.html` | Error page | 30 | Server error |

### 📂 models/ - AI Models (Generated)

| File | Description | Size | Purpose |
|------|-------------|------|---------|
| `outbreak_lr_model.pkl` | Logistic Regression | ~10KB | Outbreak prediction |
| `outbreak_rf_model.pkl` | Random Forest | ~500KB | Outbreak prediction (AI) |
| `outbreak_scaler.pkl` | Feature scaler | ~5KB | Data preprocessing |
| `patient_lr_model.pkl` | Logistic Regression | ~10KB | Patient diagnosis |
| `patient_rf_model.pkl` | Random Forest | ~400KB | Patient diagnosis (AI) |
| `patient_svm_model.pkl` | SVM | ~50KB | Patient diagnosis (AI) |
| `patient_scaler.pkl` | Feature scaler | ~5KB | Data preprocessing |

### 📂 data/ - Datasets & Visualizations (Generated)

| File | Description | Type | Purpose |
|------|-------------|------|---------|
| `outbreak_data.csv` | Environmental data | CSV | Training dataset |
| `patient_data.csv` | Clinical data | CSV | Training dataset |
| `outbreak_correlation.png` | Heatmap | Image | Feature correlations |
| `outbreak_eda.png` | EDA plots | Image | Data exploration |
| `patient_eda.png` | EDA plots | Image | Data exploration |
| `outbreak_feature_importance.png` | Bar chart | Image | AI explainability |
| `*_cm.png` | Confusion matrices | Images | Model evaluation |

---

## 🎯 FILE PURPOSES

### Core Application Files

#### 1. train_models.py
**Purpose:** Train all AI models
**What it does:**
- Generates 2000 samples per module
- Performs EDA
- Trains 5 AI models
- Saves models as .pkl files
- Creates visualizations
**Run:** `python train_models.py`
**Time:** 2-3 minutes

#### 2. app/app.py
**Purpose:** Main web application
**What it does:**
- Loads AI models
- Defines routes (/, /outbreak, /patient, /dashboard)
- Handles API requests
- Makes predictions
- Generates explanations
**Run:** `python app.py` (from app/ folder)

#### 3. app/database.py
**Purpose:** MongoDB integration
**What it does:**
- Connects to MongoDB
- Saves environmental data
- Saves patient data
- Stores predictions
- Retrieves statistics
**Used by:** app.py

### Documentation Files

#### 1. README.md
**For:** Complete project understanding
**Contains:**
- Project overview
- Features list
- Setup instructions
- Technology stack
- Learning outcomes
- Future enhancements

#### 2. QUICKSTART.md
**For:** Quick setup and testing
**Contains:**
- 5-minute setup guide
- Test cases
- Troubleshooting
- API documentation
- Tips and tricks

#### 3. PROJECT_SUMMARY.md
**For:** Technical details
**Contains:**
- Architecture overview
- AI model explanations
- API specifications
- Database schema
- Performance metrics
- Code examples

#### 4. INDEX.md (This File)
**For:** Navigation
**Contains:**
- File structure
- File descriptions
- Quick reference
- Usage guide

---

## 🔍 FINDING WHAT YOU NEED

### Want to understand the project?
→ Read `README.md`

### Want to run it quickly?
→ Follow `QUICKSTART.md`

### Want technical details?
→ Check `PROJECT_SUMMARY.md`

### Want to modify AI models?
→ Edit `train_models.py`

### Want to change web pages?
→ Edit files in `app/templates/`

### Want to add API endpoints?
→ Edit `app/app.py`

### Want to modify database?
→ Edit `app/database.py`

### Want to change styling?
→ Edit CSS in `app/templates/base.html`

---

## 📊 CODE STATISTICS

### Total Lines of Code
- **Python:** ~2,000 lines
- **HTML:** ~1,500 lines
- **JavaScript:** ~300 lines
- **CSS:** ~400 lines
- **Total:** ~4,200 lines

### Files Created
- **Python files:** 3
- **HTML templates:** 7
- **Documentation:** 4
- **Models (generated):** 7
- **Visualizations (generated):** 6+
- **Total:** 27+ files

### Features Implemented
- ✅ 2 AI modules
- ✅ 5 ML models
- ✅ 7 web pages
- ✅ 3 API endpoints
- ✅ MongoDB integration
- ✅ Real-time predictions
- ✅ AI explainability
- ✅ Interactive dashboard

---

## 🎓 LEARNING PATH

### Beginner Path
1. Read `README.md` - Understand the project
2. Follow `QUICKSTART.md` - Run the application
3. Test both modules - See AI in action
4. View dashboard - Understand statistics
5. Read code comments - Learn implementation

### Intermediate Path
1. Study `train_models.py` - Understand AI training
2. Analyze `app.py` - Learn Flask and APIs
3. Examine `database.py` - MongoDB operations
4. Modify templates - Customize UI
5. Add new features - Extend functionality

### Advanced Path
1. Implement deep learning models
2. Add real-time data integration
3. Create mobile application
4. Deploy to cloud (AWS/Azure)
5. Add advanced visualizations

---

## 🛠️ CUSTOMIZATION GUIDE

### Change AI Model Parameters
**File:** `train_models.py`
**Lines:** 200-300
**Example:**
```python
# Change Random Forest parameters
rf_model = RandomForestClassifier(
    n_estimators=200,  # Increase trees
    max_depth=15,      # Increase depth
    random_state=42
)
```

### Add New Features
**File:** `train_models.py`
**Lines:** 50-100
**Example:**
```python
# Add new feature to outbreak data
data['Wind_Speed'] = np.random.uniform(0, 50, n_samples)
```

### Modify UI Colors
**File:** `app/templates/base.html`
**Lines:** 20-30
**Example:**
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
}
```

### Add New API Endpoint
**File:** `app/app.py`
**Lines:** 400+
**Example:**
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    # Your code here
    return jsonify(response)
```

---

## 📞 TROUBLESHOOTING REFERENCE

### Issue: Models not loading
**File to check:** `train_models.py`
**Solution:** Run training script
**Command:** `python train_models.py`

### Issue: MongoDB connection error
**File to check:** `app/database.py`
**Solution:** Install/start MongoDB or continue without it
**Command:** `net start MongoDB`

### Issue: Port already in use
**File to modify:** `app/app.py`
**Line:** Last line
**Change:** `app.run(port=5001)`

### Issue: Missing dependencies
**File to check:** `requirements.txt`
**Solution:** Install packages
**Command:** `pip install -r requirements.txt`

---

## 🎯 TESTING CHECKLIST

### ✅ Setup Tests
- [ ] Dependencies installed
- [ ] Models trained successfully
- [ ] Application starts without errors
- [ ] Can access http://127.0.0.1:5000

### ✅ Functionality Tests
- [ ] Home page loads
- [ ] Outbreak prediction works
- [ ] Patient diagnosis works
- [ ] Dashboard displays data
- [ ] AI explanations appear
- [ ] Recommendations shown

### ✅ Database Tests (if MongoDB running)
- [ ] Data saves successfully
- [ ] Statistics update
- [ ] Prediction history shows
- [ ] Recent activity displays

---

## 📚 ADDITIONAL RESOURCES

### Learn More About:

**Machine Learning:**
- scikit-learn documentation
- Random Forest algorithm
- Feature importance

**Flask:**
- Flask official docs
- RESTful API design
- Jinja2 templates

**MongoDB:**
- MongoDB documentation
- pymongo tutorial
- NoSQL concepts

**Data Science:**
- pandas documentation
- Data visualization
- EDA techniques

---

## 🎉 PROJECT COMPLETION CHECKLIST

### ✅ Core Features
- [x] AI model training
- [x] Web application
- [x] Database integration
- [x] API endpoints
- [x] UI/UX design
- [x] Documentation

### ✅ AI Components
- [x] Logistic Regression
- [x] Random Forest
- [x] SVM
- [x] Feature importance
- [x] AI explainability

### ✅ Data Science
- [x] EDA
- [x] Preprocessing
- [x] Visualization
- [x] Model evaluation

### ✅ Documentation
- [x] README
- [x] Quick start guide
- [x] Project summary
- [x] Code comments
- [x] API documentation

---

## 🏆 PROJECT STATS

- **Total Development Time:** 40+ hours
- **Lines of Code:** 4,200+
- **Files Created:** 27+
- **AI Models:** 5
- **Accuracy:** 85-95%
- **Web Pages:** 7
- **API Endpoints:** 3
- **Database Collections:** 3

---

## 💡 QUICK TIPS

1. **Always train models first** before running the app
2. **Use Random Forest** for best accuracy
3. **Check AI explanations** to understand predictions
4. **View dashboard** to see system statistics
5. **Test with extreme values** to see AI behavior
6. **Read code comments** for learning
7. **Modify and experiment** to learn more

---

## 🚀 NEXT STEPS

1. ✅ Run the application
2. ✅ Test both modules
3. ✅ View dashboard
4. ✅ Read documentation
5. ✅ Understand code
6. ✅ Customize features
7. ✅ Add enhancements
8. ✅ Deploy (optional)

---

**Everything you need is in this project!**

**Ready to start? Run:** `python train_models.py`

---

**Built with ❤️ for Data Science & AI Education**
