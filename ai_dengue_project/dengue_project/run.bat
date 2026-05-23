@echo off
echo ============================================================
echo AI-POWERED DENGUE PREDICTION SYSTEM - SETUP
echo ============================================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt
echo.

echo [2/3] Training AI models...
python train_models.py
echo.

echo [3/3] Starting web application...
cd app
python app.py
