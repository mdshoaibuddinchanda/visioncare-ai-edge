"""
Database service for storing and retrieving scan data using SQLite.
"""
import os
import sqlite3
import json
from datetime import datetime
from config.settings import DATABASE_PATH


class DatabaseService:
    """Handles all database operations for VisionCare AI."""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialize database and create tables if they don't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create scans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                image_path TEXT,
                anemia_score REAL,
                jaundice_score REAL,
                redness_score REAL,
                inflammation_score REAL,
                anemia_explanation TEXT,
                jaundice_explanation TEXT,
                redness_explanation TEXT,
                inflammation_explanation TEXT,
                overall_health TEXT,
                additional_findings TEXT,
                dietary_suggestions TEXT,
                lifestyle_recommendations TEXT,
                urgent_care_needed INTEGER DEFAULT 0,
                doctor_consultation_advice TEXT,
                risk_level TEXT,
                quality_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_patient(self, name="Anonymous", age=0, gender="Not specified"):
        """Create a new patient record."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)",
            (name, age, gender)
        )
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return patient_id
    
    def save_scan(self, patient_id, image_path, analysis, quality_score=None):
        """Save a scan record with analysis results."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate risk level
        scores = [
            analysis.get("anemia_score", 0),
            analysis.get("jaundice_score", 0),
            analysis.get("redness_score", 0),
            analysis.get("inflammation_score", 0)
        ]
        max_score = max(scores)
        if max_score <= 30:
            risk_level = "Low"
        elif max_score <= 70:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Convert lists to JSON strings
        dietary = json.dumps(analysis.get("dietary_suggestions", []))
        lifestyle = json.dumps(analysis.get("lifestyle_recommendations", []))
        
        cursor.execute("""
            INSERT INTO scans (
                patient_id, image_path,
                anemia_score, jaundice_score, redness_score, inflammation_score,
                anemia_explanation, jaundice_explanation, redness_explanation, inflammation_explanation,
                overall_health, additional_findings,
                dietary_suggestions, lifestyle_recommendations,
                urgent_care_needed, doctor_consultation_advice,
                risk_level, quality_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id, image_path,
            analysis.get("anemia_score", 0),
            analysis.get("jaundice_score", 0),
            analysis.get("redness_score", 0),
            analysis.get("inflammation_score", 0),
            analysis.get("anemia_explanation", ""),
            analysis.get("jaundice_explanation", ""),
            analysis.get("redness_explanation", ""),
            analysis.get("inflammation_explanation", ""),
            analysis.get("overall_health", "unknown"),
            analysis.get("additional_findings", ""),
            dietary, lifestyle,
            1 if analysis.get("urgent_care_needed", False) else 0,
            analysis.get("doctor_consultation_advice", ""),
            risk_level,
            quality_score
        ))
        
        scan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return scan_id
    
    def get_scan_history(self, limit=20):
        """Get recent scan history."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.*, p.name as patient_name, p.age, p.gender
            FROM scans s
            LEFT JOIN patients p ON s.patient_id = p.id
            ORDER BY s.created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_scan_by_id(self, scan_id):
        """Get a specific scan by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.*, p.name as patient_name, p.age, p.gender
            FROM scans s
            LEFT JOIN patients p ON s.patient_id = p.id
            WHERE s.id = ?
        """, (scan_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_dashboard_data(self):
        """Get aggregated data for community dashboard."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        data = {}
        
        # Total scans
        cursor.execute("SELECT COUNT(*) as total FROM scans")
        data["total_scans"] = cursor.fetchone()["total"]
        
        # Total patients
        cursor.execute("SELECT COUNT(*) as total FROM patients")
        data["total_patients"] = cursor.fetchone()["total"]
        
        # Risk distribution
        cursor.execute("""
            SELECT risk_level, COUNT(*) as count 
            FROM scans 
            GROUP BY risk_level
        """)
        data["risk_distribution"] = {row["risk_level"]: row["count"] for row in cursor.fetchall()}
        for level in ["Low", "Medium", "High"]:
            if level not in data["risk_distribution"]:
                data["risk_distribution"][level] = 0
        
        # High risk cases
        cursor.execute("SELECT COUNT(*) as count FROM scans WHERE risk_level = 'High'")
        data["high_risk_cases"] = cursor.fetchone()["count"]
        
        # Monthly trends (last 6 months)
        cursor.execute("""
            SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count
            FROM scans
            WHERE created_at >= date('now', '-6 months')
            GROUP BY month
            ORDER BY month
        """)
        data["monthly_trends"] = {row["month"]: row["count"] for row in cursor.fetchall()}
        
        # Average scores
        cursor.execute("""
            SELECT 
                AVG(anemia_score) as avg_anemia,
                AVG(jaundice_score) as avg_jaundice,
                AVG(redness_score) as avg_redness,
                AVG(inflammation_score) as avg_inflammation
            FROM scans
        """)
        row = cursor.fetchone()
        if row and row["avg_anemia"]:
            data["avg_scores"] = {
                "anemia": round(row["avg_anemia"], 1),
                "jaundice": round(row["avg_jaundice"], 1),
                "redness": round(row["avg_redness"], 1),
                "inflammation": round(row["avg_inflammation"], 1)
            }
        else:
            data["avg_scores"] = {"anemia": 0, "jaundice": 0, "redness": 0, "inflammation": 0}
        
        # Recent scans
        cursor.execute("""
            SELECT s.*, p.name as patient_name
            FROM scans s
            LEFT JOIN patients p ON s.patient_id = p.id
            ORDER BY s.created_at DESC
            LIMIT 10
        """)
        data["recent_scans"] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return data
    
    def get_patient_count(self):
        """Get total number of patients."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_scan_count(self):
        """Get total number of scans."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM scans")
        count = cursor.fetchone()[0]
        conn.close()
        return count