"""
AI Model Training Script
Trains machine learning models for dengue prediction and detection

This script demonstrates:
- Data Science: EDA, preprocessing, feature engineering
- AI: Multiple algorithms, ensemble methods, model comparison
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, classification_report, 
                            confusion_matrix, roc_auc_score, roc_curve)
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

class DengueAITrainer:
    """
    AI Model Trainer for Dengue Prediction System
    
    CONCEPT: Think of this as an AI Training Academy
    - We teach multiple AI students (models) to make predictions
    - Each student learns differently (different algorithms)
    - We test them and pick the best performers
    """
    
    def __init__(self):
        self.models_dir = 'models'
        self.data_dir = 'data'
        
        # Create directories
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        print("="*70)
        print("AI-POWERED DENGUE PREDICTION SYSTEM - MODEL TRAINING")
        print("="*70)
    
    # ==========================================
    # DATA GENERATION
    # ==========================================
    
    def generate_outbreak_dataset(self, n_samples=2000):
        """
        Generate synthetic environmental data for outbreak prediction.
        
        CONCEPT: Creating Training Data
        In real projects, this would be historical weather and outbreak data.
        We're creating realistic synthetic data to demonstrate the AI system.
        
        ANALOGY: Like creating practice problems for students to learn from.
        """
        print("\n[DATA SCIENCE] Generating outbreak prediction dataset...")
        
        np.random.seed(42)
        
        # Generate features with realistic distributions
        data = {
            'Temperature': np.random.normal(30, 5, n_samples).clip(20, 40),
            'Rainfall': np.random.gamma(2, 50, n_samples).clip(0, 300),
            'Humidity': np.random.normal(70, 15, n_samples).clip(40, 100),
            'Population_Density': np.random.lognormal(7, 1, n_samples).clip(100, 5000)
        }
        
        df = pd.DataFrame(data)
        
        # Create target variable using domain knowledge
        # HIGH RISK: Hot + Rainy + Humid + Dense Population
        risk_score = (
            ((df['Temperature'] > 28) * 1.5).astype(float) +
            ((df['Rainfall'] > 150) * 2.0).astype(float) +
            ((df['Humidity'] > 70) * 1.5).astype(float) +
            ((df['Population_Density'] > 2000) * 1.0).astype(float)
        )
        
        # Add some noise for realism
        risk_score += np.random.normal(0, 0.5, n_samples)
        
        # Categorize into risk levels
        df['Risk_Level'] = pd.cut(risk_score, 
                                   bins=[-np.inf, 2.5, 5.0, np.inf], 
                                   labels=[0, 1, 2])  # 0=Low, 1=Medium, 2=High
        df['Risk_Level'] = df['Risk_Level'].astype(int)
        
        # Save dataset
        df.to_csv(f'{self.data_dir}/outbreak_data.csv', index=False)
        
        print(f"[OK] Generated {n_samples} samples")
        print(f"[OK] Risk distribution: {df['Risk_Level'].value_counts().to_dict()}")
        
        return df
    
    def generate_detection_dataset(self, n_samples=2000):
        """
        Generate synthetic symptom data for dengue detection & monitoring.
        
        CONCEPT: Creating Symptom Records
        In real hospitals, this would be actual patient symptom data.
        We simulate realistic dengue symptom patterns across 13 features.
        
        Features are grouped into:
        1. Fever Monitoring: high_fever, fever_duration_days, biphasic_fever
        2. Physical Symptoms: muscle_joint_pain, pain_behind_eyes, headache,
                              fatigue, vomiting, skin_rash
        3. Warning Signs: bleeding_signs, severe_abdominal_pain,
                          rapid_breathing, extreme_fatigue_restlessness
        
        Target: Risk Level (0=Low, 1=Moderate, 2=High)
        """
        print("\n[DATA SCIENCE] Generating dengue detection dataset...")
        
        np.random.seed(42)
        
        # --- Fever Monitoring Features ---
        high_fever = np.random.choice([0, 1], n_samples, p=[0.35, 0.65])
        fever_duration_days = np.where(
            high_fever == 1,
            np.random.choice(range(1, 15), n_samples),
            np.random.choice(range(0, 4), n_samples)
        )
        # Biphasic fever more likely when fever is present and long duration
        biphasic_prob = 0.05 + 0.3 * high_fever + 0.02 * fever_duration_days
        biphasic_fever = (np.random.random(n_samples) < biphasic_prob).astype(int)
        
        # --- Physical Symptoms ---
        muscle_joint_pain = np.random.choice([0, 1], n_samples, p=[0.40, 0.60])
        pain_behind_eyes = np.random.choice([0, 1], n_samples, p=[0.55, 0.45])
        headache = np.random.choice([0, 1], n_samples, p=[0.35, 0.65])
        fatigue = np.random.choice([0, 1], n_samples, p=[0.30, 0.70])
        vomiting = np.random.choice([0, 1], n_samples, p=[0.60, 0.40])
        skin_rash = np.random.choice([0, 1], n_samples, p=[0.65, 0.35])
        
        # --- Warning Signs ---
        bleeding_signs = np.random.choice([0, 1], n_samples, p=[0.80, 0.20])
        severe_abdominal_pain = np.random.choice([0, 1], n_samples, p=[0.75, 0.25])
        rapid_breathing = np.random.choice([0, 1], n_samples, p=[0.82, 0.18])
        extreme_fatigue_restlessness = np.random.choice([0, 1], n_samples, p=[0.78, 0.22])
        
        data = {
            'high_fever': high_fever,
            'fever_duration_days': fever_duration_days,
            'biphasic_fever': biphasic_fever,
            'muscle_joint_pain': muscle_joint_pain,
            'pain_behind_eyes': pain_behind_eyes,
            'headache': headache,
            'fatigue': fatigue,
            'vomiting': vomiting,
            'skin_rash': skin_rash,
            'bleeding_signs': bleeding_signs,
            'severe_abdominal_pain': severe_abdominal_pain,
            'rapid_breathing': rapid_breathing,
            'extreme_fatigue_restlessness': extreme_fatigue_restlessness
        }
        
        df = pd.DataFrame(data)
        
        # Create risk score using medical domain knowledge
        risk_score = (
            high_fever * 1.5 +
            (fever_duration_days >= 3).astype(float) * 1.0 +
            biphasic_fever * 1.5 +
            muscle_joint_pain * 0.8 +
            pain_behind_eyes * 0.7 +
            headache * 0.5 +
            fatigue * 0.4 +
            vomiting * 0.6 +
            skin_rash * 0.5 +
            bleeding_signs * 2.0 +
            severe_abdominal_pain * 1.8 +
            rapid_breathing * 1.5 +
            extreme_fatigue_restlessness * 1.2
        )
        
        # Add noise
        risk_score += np.random.normal(0, 0.5, n_samples)
        
        # 3-class risk: Low / Moderate / High
        df['Risk_Level'] = pd.cut(
            risk_score,
            bins=[-np.inf, 3.5, 7.0, np.inf],
            labels=[0, 1, 2]
        )
        df['Risk_Level'] = df['Risk_Level'].astype(int)
        
        # Save dataset
        df.to_csv(f'{self.data_dir}/detection_data.csv', index=False)
        
        print(f"[OK] Generated {n_samples} samples with 13 features")
        print(f"[OK] Risk distribution: {df['Risk_Level'].value_counts().to_dict()}")
        
        return df
    
    # ==========================================
    # EXPLORATORY DATA ANALYSIS (EDA)
    # ==========================================
    
    def perform_eda_outbreak(self, df):
        """
        Exploratory Data Analysis for outbreak data.
        
        CONCEPT: Understanding Your Data
        Before training AI, we must understand patterns in data.
        Like a detective examining clues before solving a case.
        """
        print("\n[DATA SCIENCE] Performing EDA on outbreak data...")
        
        # Statistical summary
        print("\nStatistical Summary:")
        print(df.describe())
        
        # Correlation analysis
        print("\nFeature Correlations with Risk:")
        correlations = df.corr()['Risk_Level'].sort_values(ascending=False)
        print(correlations)
        
        # Visualization 1: Correlation Heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title('Feature Correlation Heatmap - Outbreak Data')
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/outbreak_correlation.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: outbreak_correlation.png")
        
        # Visualization 2: Risk Distribution
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        features = ['Temperature', 'Rainfall', 'Humidity', 'Population_Density']
        
        for idx, feature in enumerate(features):
            row, col = idx // 3, idx % 3
            for risk in [0, 1, 2]:
                data = df[df['Risk_Level'] == risk][feature]
                axes[row, col].hist(data, alpha=0.5, label=f'Risk {risk}', bins=20)
            axes[row, col].set_title(f'{feature} by Risk Level')
            axes[row, col].set_xlabel(feature)
            axes[row, col].legend()
        
        axes[1, 1].pie(df['Risk_Level'].value_counts(), labels=['Low', 'Medium', 'High'],
                       autopct='%1.1f%%', colors=['green', 'orange', 'red'])
        axes[1, 1].set_title('Risk Level Distribution')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/outbreak_eda.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: outbreak_eda.png")
    
    def perform_eda_detection(self, df):
        """
        Exploratory Data Analysis for detection symptom data.
        
        CONCEPT: Understanding Symptom Patterns
        We analyze how different symptoms correlate with dengue risk.
        """
        print("\n[DATA SCIENCE] Performing EDA on detection data...")
        
        # Statistical summary
        print("\nStatistical Summary:")
        print(df.describe())
        
        # Correlation analysis
        print("\nFeature Correlations with Risk Level:")
        correlations = df.corr()['Risk_Level'].sort_values(ascending=False)
        print(correlations)
        
        # Visualization 1: Symptom Correlation Heatmap
        plt.figure(figsize=(14, 10))
        sns.heatmap(df.corr(), annot=True, cmap='YlOrRd', center=0, fmt='.2f',
                    linewidths=0.5)
        plt.title('Symptom Correlation Heatmap - Dengue Detection')
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/detection_correlation.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: detection_correlation.png")
        
        # Visualization 2: Symptom prevalence by risk level
        symptom_cols = [c for c in df.columns if c != 'Risk_Level' and c != 'fever_duration_days']
        fig, axes = plt.subplots(3, 4, figsize=(18, 12))
        
        for idx, col in enumerate(symptom_cols):
            row, col_idx = idx // 4, idx % 4
            symptom_by_risk = df.groupby('Risk_Level')[col].mean()
            colors = ['#10b981', '#f59e0b', '#ef4444']
            axes[row, col_idx].bar(['Low', 'Moderate', 'High'], symptom_by_risk.values, color=colors)
            axes[row, col_idx].set_title(col.replace('_', ' ').title(), fontsize=10)
            axes[row, col_idx].set_ylim(0, 1)
            axes[row, col_idx].set_ylabel('Prevalence')
        
        # Last subplot: Risk distribution
        axes[2, 3].pie(df['Risk_Level'].value_counts().sort_index(),
                       labels=['Low', 'Moderate', 'High'],
                       autopct='%1.1f%%', colors=['#10b981', '#f59e0b', '#ef4444'])
        axes[2, 3].set_title('Risk Level Distribution')
        
        plt.suptitle('Symptom Prevalence by Dengue Risk Level', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/detection_eda.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: detection_eda.png")
    
    # ==========================================
    # MODEL TRAINING - OUTBREAK PREDICTION
    # ==========================================
    
    def train_outbreak_models(self, df):
        """
        Train AI models for outbreak prediction.
        
        CONCEPT: Teaching AI to Predict Outbreaks
        We train two types of AI:
        1. Logistic Regression - Simple, fast (baseline)
        2. Random Forest - Advanced, accurate (ensemble AI)
        
        ANALOGY: Training two weather forecasters
        - One uses simple rules (Logistic Regression)
        - One consults 100 experts and votes (Random Forest)
        """
        print("\n" + "="*70)
        print("[AI TRAINING] OUTBREAK PREDICTION MODELS")
        print("="*70)
        
        # Prepare data
        X = df.drop('Risk_Level', axis=1)
        y = df['Risk_Level']
        
        # Split data: 80% training, 20% testing
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n[DATA] Training samples: {len(X_train)}")
        print(f"[DATA] Testing samples: {len(X_test)}")
        
        # Feature Scaling
        print("\n[PREPROCESSING] Scaling features...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Save scaler
        joblib.dump(scaler, f'{self.models_dir}/outbreak_scaler.pkl')
        
        # Model 1: Logistic Regression (Baseline)
        print("\n[AI MODEL 1] Training Logistic Regression...")
        print("CONCEPT: Simple linear decision boundaries")
        print("ANALOGY: Drawing straight lines to separate risk zones")
        
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(X_train_scaled, y_train)
        
        lr_pred = lr_model.predict(X_test_scaled)
        lr_accuracy = accuracy_score(y_test, lr_pred)
        
        print(f"[RESULT] Accuracy: {lr_accuracy:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, lr_pred, target_names=['Low', 'Medium', 'High']))
        
        # Save model
        joblib.dump(lr_model, f'{self.models_dir}/outbreak_lr_model.pkl')
        
        # Model 2: Random Forest (Advanced AI)
        print("\n[AI MODEL 2] Training Random Forest...")
        print("CONCEPT: Ensemble of 100 decision trees voting together")
        print("ANALOGY: Asking 100 experts and taking majority opinion")
        
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        rf_model.fit(X_train_scaled, y_train)
        
        rf_pred = rf_model.predict(X_test_scaled)
        rf_accuracy = accuracy_score(y_test, rf_pred)
        
        print(f"[RESULT] Accuracy: {rf_accuracy:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, rf_pred, target_names=['Low', 'Medium', 'High']))
        
        # Feature Importance (AI Explainability)
        print("\n[AI EXPLAINABILITY] Feature Importance:")
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': rf_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        print(feature_importance)
        
        # Visualize feature importance
        plt.figure(figsize=(10, 6))
        plt.barh(feature_importance['Feature'], feature_importance['Importance'])
        plt.xlabel('Importance Score')
        plt.title('Feature Importance - Outbreak Prediction AI')
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/outbreak_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: outbreak_feature_importance.png")
        
        # Save model
        joblib.dump(rf_model, f'{self.models_dir}/outbreak_rf_model.pkl')
        
        # Confusion Matrix
        self._plot_confusion_matrix(y_test, rf_pred, ['Low', 'Medium', 'High'],
                                   'Outbreak Prediction - Random Forest')
        
        print("\n[SUCCESS] Outbreak prediction models trained and saved!")
        
        return {
            'lr_accuracy': lr_accuracy,
            'rf_accuracy': rf_accuracy,
            'feature_importance': feature_importance
        }
    
    # ==========================================
    # MODEL TRAINING - DENGUE DETECTION
    # ==========================================
    
    def train_detection_models(self, df):
        """
        Train AI models for dengue detection & monitoring.
        
        CONCEPT: Teaching AI to Detect Dengue from Symptoms
        We train three AI models on 13 symptom features:
        1. Logistic Regression - Fast baseline
        2. Random Forest - Comprehensive analysis
        3. SVM - Pattern recognition expert
        
        Target: 3-class risk (Low / Moderate / High)
        """
        print("\n" + "="*70)
        print("[AI TRAINING] DENGUE DETECTION MODELS")
        print("="*70)
        
        # Prepare data
        X = df.drop('Risk_Level', axis=1)
        y = df['Risk_Level']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n[DATA] Training samples: {len(X_train)}")
        print(f"[DATA] Testing samples: {len(X_test)}")
        print(f"[DATA] Features: {list(X.columns)}")
        
        # Feature Scaling
        print("\n[PREPROCESSING] Scaling features...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Save scaler
        joblib.dump(scaler, f'{self.models_dir}/detection_scaler.pkl')
        
        results = {}
        
        # Model 1: Logistic Regression
        print("\n[AI MODEL 1] Training Logistic Regression...")
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(X_train_scaled, y_train)
        
        lr_pred = lr_model.predict(X_test_scaled)
        lr_accuracy = accuracy_score(y_test, lr_pred)
        results['lr_accuracy'] = lr_accuracy
        
        print(f"[RESULT] Accuracy: {lr_accuracy:.2%}")
        print(classification_report(y_test, lr_pred, target_names=['Low', 'Moderate', 'High']))
        
        joblib.dump(lr_model, f'{self.models_dir}/detection_lr_model.pkl')
        
        # Model 2: Random Forest
        print("\n[AI MODEL 2] Training Random Forest...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        rf_model.fit(X_train_scaled, y_train)
        
        rf_pred = rf_model.predict(X_test_scaled)
        rf_accuracy = accuracy_score(y_test, rf_pred)
        results['rf_accuracy'] = rf_accuracy
        
        print(f"[RESULT] Accuracy: {rf_accuracy:.2%}")
        print(classification_report(y_test, rf_pred, target_names=['Low', 'Moderate', 'High']))
        
        # Feature Importance
        print("\n[AI EXPLAINABILITY] Feature Importance:")
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': rf_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        print(feature_importance)
        
        # Visualize feature importance
        plt.figure(figsize=(12, 7))
        colors = ['#ef4444' if imp > 0.1 else '#f59e0b' if imp > 0.06 else '#10b981'
                  for imp in feature_importance['Importance'].values]
        plt.barh(feature_importance['Feature'].str.replace('_', ' ').str.title(),
                 feature_importance['Importance'], color=colors)
        plt.xlabel('Importance Score')
        plt.title('Feature Importance - Dengue Detection AI')
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/detection_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: detection_feature_importance.png")
        
        joblib.dump(rf_model, f'{self.models_dir}/detection_rf_model.pkl')
        
        # Model 3: SVM
        print("\n[AI MODEL 3] Training Support Vector Machine...")
        print("CONCEPT: Finds optimal boundaries between risk levels in feature space")
        svm_model = SVC(kernel='rbf', probability=True, random_state=42)
        svm_model.fit(X_train_scaled, y_train)
        
        svm_pred = svm_model.predict(X_test_scaled)
        svm_accuracy = accuracy_score(y_test, svm_pred)
        results['svm_accuracy'] = svm_accuracy
        
        print(f"[RESULT] Accuracy: {svm_accuracy:.2%}")
        print(classification_report(y_test, svm_pred, target_names=['Low', 'Moderate', 'High']))
        
        joblib.dump(svm_model, f'{self.models_dir}/detection_svm_model.pkl')
        
        # Confusion Matrix for best model (RF)
        self._plot_confusion_matrix(y_test, rf_pred, ['Low', 'Moderate', 'High'],
                                   'Dengue Detection - Random Forest')
        
        print("\n[SUCCESS] Dengue detection models trained and saved!")
        
        return results
    
    # ==========================================
    # UTILITY FUNCTIONS
    # ==========================================
    
    def _plot_confusion_matrix(self, y_true, y_pred, labels, title):
        """
        Plot confusion matrix.
        
        CONCEPT: Visual Report Card for AI
        Shows where AI is correct and where it makes mistakes.
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=labels, yticklabels=labels)
        plt.title(f'Confusion Matrix - {title}')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        
        filename = title.lower().replace(' ', '_').replace('-', '') + '_cm.png'
        plt.savefig(f'{self.data_dir}/{filename}', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] Saved: {filename}")

# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    """
    Main training pipeline
    """
    trainer = DengueAITrainer()
    
    # Step 1: Generate datasets
    print("\n" + "="*70)
    print("STEP 1: DATA GENERATION")
    print("="*70)
    outbreak_df = trainer.generate_outbreak_dataset(n_samples=2000)
    detection_df = trainer.generate_detection_dataset(n_samples=2000)
    
    # Step 2: Exploratory Data Analysis
    print("\n" + "="*70)
    print("STEP 2: EXPLORATORY DATA ANALYSIS (EDA)")
    print("="*70)
    trainer.perform_eda_outbreak(outbreak_df)
    trainer.perform_eda_detection(detection_df)
    
    # Step 3: Train outbreak models
    print("\n" + "="*70)
    print("STEP 3: AI MODEL TRAINING - OUTBREAK PREDICTION")
    print("="*70)
    outbreak_results = trainer.train_outbreak_models(outbreak_df)
    
    # Step 4: Train detection models
    print("\n" + "="*70)
    print("STEP 4: AI MODEL TRAINING - DENGUE DETECTION")
    print("="*70)
    detection_results = trainer.train_detection_models(detection_df)
    
    # Final Summary
    print("\n" + "="*70)
    print("TRAINING COMPLETE - FINAL SUMMARY")
    print("="*70)
    
    print("\n[OUTBREAK PREDICTION MODELS]")
    print(f"  Logistic Regression: {outbreak_results['lr_accuracy']:.2%}")
    print(f"  Random Forest (AI):  {outbreak_results['rf_accuracy']:.2%}")
    
    print("\n[DENGUE DETECTION MODELS]")
    print(f"  Logistic Regression: {detection_results['lr_accuracy']:.2%}")
    print(f"  Random Forest (AI):  {detection_results['rf_accuracy']:.2%}")
    print(f"  SVM (AI):            {detection_results['svm_accuracy']:.2%}")
    
    print("\n[FILES SAVED]")
    print(f"  Models: {trainer.models_dir}/")
    print(f"  Data & Visualizations: {trainer.data_dir}/")
    
    print("\n[NEXT STEP]")
    print("  Run the web application: cd app && python app.py")
    
    print("\n" + "="*70)
    print("[SUCCESS] AI TRAINING PIPELINE COMPLETED!")
    print("="*70)

if __name__ == "__main__":
    main()
