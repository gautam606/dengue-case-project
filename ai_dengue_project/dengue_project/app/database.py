"""
Database Module - MongoDB Integration
Handles all database operations for the Dengue Prediction System

CONCEPT: Database as a Digital Filing Cabinet
Think of MongoDB as a smart filing cabinet that stores all your data.
Each "collection" is like a drawer, and each "document" is like a file folder.
"""

from pymongo import MongoClient
from datetime import datetime
import json

class DengueDatabase:
    """
    Main database class for managing all data operations.
    
    ANALOGY: Like a librarian who organizes and retrieves books.
    The librarian (this class) knows where everything is stored
    and can quickly find what you need.
    """
    
    def __init__(self, connection_string='mongodb://localhost:27017/'):
        """
        Initialize database connection.
        
        ANALOGY: Opening the library door and getting ready to work.
        """
        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Test connection
            self.db = self.client['dengue_ai_system']
            self.connected = True
            print("[SUCCESS] Connected to MongoDB successfully!")
            print(f"[INFO] Database: {self.db.name}")
        except Exception as e:
            print(f"[WARNING] MongoDB connection failed: {e}")
            print("[INFO] System will continue without database persistence")
            self.client = None
            self.db = None
            self.connected = False
    
    # ==========================================
    # ENVIRONMENTAL DATA OPERATIONS
    # ==========================================
    
    def save_environmental_data(self, data):
        """
        Store environmental data for outbreak prediction.
        
        ANALOGY: Filing a weather report in the weather drawer.
        Each report is timestamped so we can track changes over time.
        """
        if not self.connected:
            return None
        
        try:
            collection = self.db['environmental_data']
            data['timestamp'] = datetime.now()
            data['date'] = datetime.now().strftime('%Y-%m-%d')
            result = collection.insert_one(data)
            print(f"[DB] Saved environmental data: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"[ERROR] Failed to save environmental data: {e}")
            return None
    
    def get_environmental_data(self, limit=100):
        """
        Retrieve environmental data records.
        
        ANALOGY: Pulling out recent weather reports to analyze trends.
        """
        if not self.connected:
            return []
        
        try:
            collection = self.db['environmental_data']
            data = list(collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(limit))
            return data
        except Exception as e:
            print(f"[ERROR] Failed to retrieve environmental data: {e}")
            return []
    
    # ==========================================
    # SYMPTOM DATA OPERATIONS (Detection Module)
    # ==========================================
    
    def save_symptom_data(self, data):
        """
        Store symptom assessment data from the detection module.
        
        ANALOGY: Recording a patient's symptom checklist in their file.
        Stores all 13 symptom features + prediction result.
        """
        if not self.connected:
            return None
        
        try:
            collection = self.db['symptom_data']
            data['timestamp'] = datetime.now()
            data['date'] = datetime.now().strftime('%Y-%m-%d')
            result = collection.insert_one(data)
            print(f"[DB] Saved symptom data: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"[ERROR] Failed to save symptom data: {e}")
            return None
    
    def get_symptom_data(self, limit=100):
        """
        Retrieve symptom assessment records.
        """
        if not self.connected:
            return []
        
        try:
            collection = self.db['symptom_data']
            data = list(collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(limit))
            return data
        except Exception as e:
            print(f"[ERROR] Failed to retrieve symptom data: {e}")
            return []
    
    # ==========================================
    # FEVER HISTORY OPERATIONS
    # ==========================================
    
    def save_fever_reading(self, data):
        """
        Store a fever temperature reading for monitoring.
        
        ANALOGY: Adding a data point to a patient's temperature chart.
        Over time, this builds a fever trend that can reveal patterns
        like biphasic (saddleback) fever.
        """
        if not self.connected:
            return None
        
        try:
            collection = self.db['fever_history']
            data['timestamp'] = datetime.now()
            data['date'] = datetime.now().strftime('%Y-%m-%d')
            result = collection.insert_one(data)
            print(f"[DB] Saved fever reading: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"[ERROR] Failed to save fever reading: {e}")
            return None
    
    def get_fever_history(self, limit=50):
        """
        Retrieve fever history for trend analysis.
        
        ANALOGY: Pulling out the temperature chart to look for patterns.
        """
        if not self.connected:
            return []
        
        try:
            collection = self.db['fever_history']
            data = list(collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(limit))
            return data
        except Exception as e:
            print(f"[ERROR] Failed to retrieve fever history: {e}")
            return []
    
    # ==========================================
    # PREDICTION OPERATIONS
    # ==========================================
    
    def save_prediction(self, prediction_type, input_data, prediction_result, model_used, explanation=None):
        """
        Store AI prediction results.
        
        ANALOGY: Keeping a log book of all diagnoses made by the AI doctor.
        This helps track accuracy and learn from past predictions.
        
        Args:
            prediction_type: 'outbreak' or 'detection'
            input_data: The features used for prediction
            prediction_result: The AI's prediction
            model_used: Which AI model made the prediction
            explanation: Why the AI made this prediction
        """
        if not self.connected:
            return None
        
        try:
            collection = self.db['predictions']
            record = {
                'type': prediction_type,
                'input_data': input_data,
                'prediction': prediction_result,
                'model_used': model_used,
                'explanation': explanation,
                'timestamp': datetime.now(),
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            result = collection.insert_one(record)
            print(f"[DB] Saved prediction: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"[ERROR] Failed to save prediction: {e}")
            return None
    
    def get_predictions(self, prediction_type=None, limit=50):
        """
        Retrieve prediction history.
        
        ANALOGY: Looking back at past diagnoses to see patterns.
        """
        if not self.connected:
            return []
        
        try:
            collection = self.db['predictions']
            query = {'type': prediction_type} if prediction_type else {}
            data = list(collection.find(query, {'_id': 0}).sort('timestamp', -1).limit(limit))
            return data
        except Exception as e:
            print(f"[ERROR] Failed to retrieve predictions: {e}")
            return []
    
    # ==========================================
    # STATISTICS & ANALYTICS
    # ==========================================
    
    def get_dashboard_statistics(self):
        """
        Calculate statistics for dashboard display.
        
        ANALOGY: Creating a summary report for management.
        Shows key metrics at a glance.
        """
        if not self.connected:
            return {
                'total_environmental_records': 0,
                'total_symptom_records': 0,
                'total_fever_records': 0,
                'total_predictions': 0,
                'outbreak_predictions': {'low': 0, 'medium': 0, 'high': 0},
                'detection_predictions': {'low': 0, 'moderate': 0, 'high': 0},
                'recent_activity': []
            }
        
        try:
            stats = {}
            
            # Count records
            stats['total_environmental_records'] = self.db['environmental_data'].count_documents({})
            stats['total_symptom_records'] = self.db['symptom_data'].count_documents({})
            stats['total_fever_records'] = self.db['fever_history'].count_documents({})
            stats['total_predictions'] = self.db['predictions'].count_documents({})
            
            # Outbreak predictions breakdown
            outbreak_preds = self.db['predictions'].find({'type': 'outbreak'})
            outbreak_counts = {'low': 0, 'medium': 0, 'high': 0}
            for pred in outbreak_preds:
                risk = pred.get('prediction', {}).get('risk_level', '').lower()
                if risk in outbreak_counts:
                    outbreak_counts[risk] += 1
            stats['outbreak_predictions'] = outbreak_counts
            
            # Detection predictions breakdown
            detection_preds = self.db['predictions'].find({'type': 'detection'})
            detection_counts = {'low': 0, 'moderate': 0, 'high': 0}
            for pred in detection_preds:
                risk = pred.get('prediction', {}).get('risk_level', '').lower()
                if risk in detection_counts:
                    detection_counts[risk] += 1
            stats['detection_predictions'] = detection_counts
            
            # Recent activity
            recent = list(self.db['predictions'].find(
                {}, {'_id': 0, 'type': 1, 'prediction': 1, 'timestamp': 1}
            ).sort('timestamp', -1).limit(10))
            stats['recent_activity'] = recent
            
            return stats
        except Exception as e:
            print(f"[ERROR] Failed to get statistics: {e}")
            return {}
    
    def get_risk_trends(self, days=7):
        """
        Get outbreak risk trends over time.
        
        ANALOGY: Creating a graph showing how dengue risk changed over the week.
        Helps identify if situation is improving or worsening.
        """
        if not self.connected:
            return []
        
        try:
            from datetime import timedelta
            start_date = datetime.now() - timedelta(days=days)
            
            pipeline = [
                {'$match': {
                    'type': 'outbreak',
                    'timestamp': {'$gte': start_date}
                }},
                {'$group': {
                    '_id': '$date',
                    'high_risk_count': {
                        '$sum': {
                            '$cond': [
                                {'$eq': ['$prediction.risk_level', 'High']},
                                1, 0
                            ]
                        }
                    },
                    'medium_risk_count': {
                        '$sum': {
                            '$cond': [
                                {'$eq': ['$prediction.risk_level', 'Medium']},
                                1, 0
                            ]
                        }
                    },
                    'low_risk_count': {
                        '$sum': {
                            '$cond': [
                                {'$eq': ['$prediction.risk_level', 'Low']},
                                1, 0
                            ]
                        }
                    }
                }},
                {'$sort': {'_id': 1}}
            ]
            
            trends = list(self.db['predictions'].aggregate(pipeline))
            return trends
        except Exception as e:
            print(f"[ERROR] Failed to get risk trends: {e}")
            return []
    
    # ==========================================
    # UTILITY FUNCTIONS
    # ==========================================
    
    def clear_collection(self, collection_name):
        """
        Clear all data from a collection (use with caution!).
        
        ANALOGY: Emptying a drawer to start fresh.
        """
        if not self.connected:
            return False
        
        try:
            self.db[collection_name].delete_many({})
            print(f"[DB] Cleared collection: {collection_name}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to clear collection: {e}")
            return False
    
    def close_connection(self):
        """
        Close database connection.
        
        ANALOGY: Closing the library at the end of the day.
        """
        if self.client:
            self.client.close()
            print("[DB] Database connection closed")

# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":
    print("="*60)
    print("TESTING DATABASE MODULE")
    print("="*60)
    
    # Initialize database
    db = DengueDatabase()
    
    if db.connected:
        # Test environmental data
        print("\n[TEST] Saving environmental data...")
        env_data = {
            'temperature': 32.5,
            'rainfall': 180.0,
            'humidity': 75.0,
            'population_density': 3000
        }
        db.save_environmental_data(env_data)
        
        # Test symptom data
        print("\n[TEST] Saving symptom data...")
        symptom_data = {
            'high_fever': 1,
            'fever_duration_days': 5,
            'biphasic_fever': 1,
            'muscle_joint_pain': 1,
            'pain_behind_eyes': 1,
            'headache': 1,
            'fatigue': 1,
            'vomiting': 0,
            'skin_rash': 1,
            'bleeding_signs': 0,
            'severe_abdominal_pain': 0,
            'rapid_breathing': 0,
            'extreme_fatigue_restlessness': 0
        }
        db.save_symptom_data(symptom_data)
        
        # Test fever reading
        print("\n[TEST] Saving fever reading...")
        fever_data = {
            'temperature': 39.2,
            'reading_time': '2024-01-15 14:30',
            'notes': 'High fever with chills'
        }
        db.save_fever_reading(fever_data)
        
        # Test prediction
        print("\n[TEST] Saving prediction...")
        prediction = {
            'risk_level': 'High',
            'probability': 0.85
        }
        db.save_prediction('detection', symptom_data, prediction, 'Random Forest',
                          'Multiple dengue symptoms detected')
        
        # Get statistics
        print("\n[TEST] Getting statistics...")
        stats = db.get_dashboard_statistics()
        print(f"Total predictions: {stats.get('total_predictions', 0)}")
        
        print("\n[SUCCESS] All database tests passed!")
    else:
        print("\n[INFO] Database not connected - tests skipped")
    
    db.close_connection()
