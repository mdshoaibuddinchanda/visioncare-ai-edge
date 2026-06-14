-- VisionCare AI Database Schema
-- SQLite

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scans table
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
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_scans_patient_id ON scans(patient_id);
CREATE INDEX IF NOT EXISTS idx_scans_created_at ON scans(created_at);
CREATE INDEX IF NOT EXISTS idx_scans_risk_level ON scans(risk_level);
CREATE INDEX IF NOT EXISTS idx_patients_created_at ON patients(created_at);