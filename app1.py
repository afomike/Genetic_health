

Create a table for doctors
CREATE table doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    license_number VARCHAR(255) NOT NULL,
    medical_school VARCHAR(255) NOT NULL,
    graduation_year INT NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    hospital_affiliation VARCHAR(255) NOT NULL,
    years_experience INT NOT NULL,
    medical_association VARCHAR(255),
    reference_contact VARCHAR(255),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Create the database
CREATE DATABASE IF NOT EXISTS healthcare_system;
USE healthcare_system;

Create a table for patients
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    age VARCHAR(255) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    contact_info VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    LGA VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    );
# name, age, gender, contact_info, state, LGA, address
Create a table for diseases
CREATE TABLE IF NOT EXISTS diseases (
    disease_id INT PRIMARY KEY AUTO_INCREMENT,
    disease_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

Create a table for diagnoses
CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    disease_id INT NOT NULL,
    symptom_1 VARCHAR(255),
    symptom_2 VARCHAR(255),
    symptom_3 VARCHAR(255),
    symptom_4 VARCHAR(255),
    symptom_5 VARCHAR(255),
    symptom_6 VARCHAR(255),
    symptom_7 VARCHAR(255),
    symptom_8 VARCHAR(255),
    symptom_9 VARCHAR(255),
    symptom_10 VARCHAR(255),
    symptom_11 VARCHAR(255),
    symptom_12 VARCHAR(255),
    symptom_13 VARCHAR(255),
    symptom_14 VARCHAR(255),
    diagnosis TEXT NOT NULL,
    test_results TEXT,
    medications TEXT,
    additional_comments TEXT,
    diagnosis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (disease_id) REFERENCES diseases(disease_id) ON DELETE CASCADE
);
