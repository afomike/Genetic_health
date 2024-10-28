from flask import Flask, request, render_template, jsonify, session, redirect, url_for, request, flash
import mysql.connector
import os 
import pandas as pd
import MySQLdb as mysqlclient
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import shutil
import numpy as np
from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime



app = Flask(__name__)

app.secret_key = os.urandom(24).hex()

# Host: sql12.freesqldatabase.com
# Database name: sql12740499
# Database user: sql12740499
# Database password: ee3HbyjLLH
# Port number: 3306

# Database connection setup
# def get_db_connection():
#     return mysql.connector.connect(
#         host="sql12.freesqldatabase.com",
#         user="sql12740499",
#         password="yourpassword",
#         database="sql12740499"
#     )
# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "sql12.freesqldatabase.com"),
        user=os.getenv("DB_USER", "sql12740499"),
        password=os.getenv("DB_PASSWORD", "ee3HbyjLLH"),
        database=os.getenv("DB_NAME", "sql12740499")
    )

@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        mydb = get_db_connection()  # Establish connection
        mycursor = mydb.cursor()  # Create a cursor

        try:
            # Retrieve form data
            full_name = request.form['full_name']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']
            license_number = request.form['license_number']
            medical_school = request.form['medical_school']
            graduation_year = request.form['graduation_year']
            specialization = request.form['specialization']
            hospital_affiliation = request.form['hospital_affiliation']
            years_experience = request.form['years_experience']
            medical_association = request.form['medical_association']
            reference_contact = request.form['reference_contact']
            
            # Hash the password for security
            hashed_password = generate_password_hash(password)

            # Insert doctor data into the database
            sql = """
            INSERT INTO doctors (full_name, email, password, phone, license_number, medical_school, graduation_year,
                                specialization, hospital_affiliation, years_experience, medical_association, reference_contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            val = (full_name, email, hashed_password, phone, license_number, medical_school, graduation_year,
                specialization, hospital_affiliation, years_experience, medical_association, reference_contact)
            
            mycursor.execute(sql, val)
            mydb.commit()

            return jsonify({"message": "Doctor registration successful!"}), 201

        except mysql.connector.Error as err:
            # Rollback in case of error and report it
            mydb.rollback()
            return jsonify({"error": str(err)}), 500

        finally:
            # Ensure the database connection is closed
            mycursor.close()
            mydb.close()

    return render_template('index.html')

#Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve email and password from the form
        email = request.form['email']
        password = request.form['password']

        # Connect to the database
        mydb = get_db_connection()
        mycursor = mydb.cursor()

        # Fetch the doctor record by email
        mycursor.execute("SELECT doctor_id, password, full_name FROM doctors WHERE email = %s", (email,))
        doctor = mycursor.fetchone()

        if doctor:
            doctor_id, hashed_password, full_name = doctor
            
            # Check if the password matches the hashed password in the database
            if check_password_hash(hashed_password, password):
                # Store doctor_id in session and log them in
                session['doctor_id'] = doctor_id
                session['full_name'] = full_name
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
        else:
            flash('Email not found.', 'danger')
        
        mycursor.close()
        mydb.close()

    return render_template('index.html')

# Dashboard route for demonstration
@app.route('/dashboard')
def dashboard():
    if 'doctor_id' in session:
        # return "Welcome to the dashboard! You are logged in as doctor_id: " + str(session['doctor_id'])
        return render_template('dashboard.html', full_name=session['full_name'])
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('doctor_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/submit_diagnosis', methods=['POST'])
def submit_diagnosis():
    try:
        # Connect to the database
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        
        # Retrieve form data
        patient_name = request.form['patient_name']
        age = request.form['age']
        gender = request.form['gender']
        num = request.form['num']
        state = request.form['state']
        LGA = request.form['LGA']
        address = request.form['address']
        disease_name = request.form['disease']
        diagnosis = request.form['diagnosis']
        test_results = request.form['test_results']
        medications = request.form['medications']
        additional_comments = request.form['additional_comments']
        
        # Retrieve each symptom field explicitly
        symptom_1 = request.form.get('symptom_1')
        symptom_2 = request.form.get('symptom_2')
        symptom_3 = request.form.get('symptom_3')
        symptom_4 = request.form.get('symptom_4')
        symptom_5 = request.form.get('symptom_5')
        symptom_6 = request.form.get('symptom_6')
        symptom_7 = request.form.get('symptom_7')
        symptom_8 = request.form.get('symptom_8')
        symptom_9 = request.form.get('symptom_9')
        symptom_10 = request.form.get('symptom_10')

        # Insert patient information
        sql_patient = "INSERT INTO patients (name, age, gender, contact_info, state, LGA, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val_patient = (patient_name, age, gender, num, state, LGA, address)
        mycursor.execute(sql_patient, val_patient)
        
        # Get the newly inserted patient_id
        patient_id = mycursor.lastrowid
        
        # Insert disease information if not already present
        sql_disease = "INSERT INTO diseases (disease_name) VALUES (%s) ON DUPLICATE KEY UPDATE disease_id=LAST_INSERT_ID(disease_id)"
        val_disease = (disease_name,)
        mycursor.execute(sql_disease, val_disease)
        
        # Get the disease_id
        disease_id = mycursor.lastrowid
        
        # Insert diagnosis along with test results, medications, and additional comments
        sql_diagnosis = """
        INSERT INTO diagnoses (patient_id, disease_id, symptom_1, symptom_2, symptom_3, symptom_4, symptom_5, 
                               symptom_6, symptom_7, symptom_8, symptom_9, symptom_10, diagnosis, test_results, medications, additional_comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val_diagnosis = (
            patient_id, disease_id, symptom_1, symptom_2, symptom_3, symptom_4, symptom_5, 
            symptom_6, symptom_7, symptom_8, symptom_9, symptom_10, diagnosis, test_results, 
            medications, additional_comments
        )
        mycursor.execute(sql_diagnosis, val_diagnosis)

        # Commit the transaction
        mydb.commit()
        flash(f"Diagnosis for {patient_name} has been recorded successfully!")
        # return f"Diagnosis for {patient_name} has been recorded successfully!"
        return render_template('dashboard.html', patients=f"Diagnosis for {patient_name} has been recorded successfully!")

    
    except Exception as e:
        # Rollback any changes if an error occurs
        mydb.rollback()
        flash(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    
    finally:
        # Close cursor and database connection
        mycursor.close()
        mydb.close()

# Route to display tables in HTML format
from flask import request, jsonify, flash, render_template

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    try:
        # Connect to the database
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)

        if request.method == 'POST':
            # Future implementation for handling POST data (optional)
            # For now, it’s just here to support POST requests without further action.
            flash("POST request received, but no data handling is implemented.")
        
        # Fetch all records for displaying
        mycursor.execute("SELECT * FROM patients")
        patients = mycursor.fetchall()

        mycursor.execute("SELECT * FROM diseases")
        diseases = mycursor.fetchall()

        mycursor.execute("SELECT * FROM diagnoses")
        diagnoses = mycursor.fetchall()

        return render_template('view.html', full_name=session['full_name'],  patients=patients, diseases=diseases, diagnoses=diagnoses)

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

    finally:
        mycursor.close()
        mydb.close()


# Route to delete an entry
@app.route('/delete/<table>/<int:id>')
def delete_entry(table, id):
    # Whitelist valid table names and map each to its primary key column
    table_primary_keys = {
        "patients": "patient_id",
        "diagnoses": "diagnosis_id",
        "diseases": "disease_id"
        # Add other tables and their primary keys as needed
    }

    if table not in table_primary_keys:
        return "Invalid table name", 400

    try:
        mydb = get_db_connection()
        mycursor = mydb.cursor()

        # Get the correct primary key column for the specified table
        primary_key_column = table_primary_keys[table]
        sql = f"DELETE FROM {table} WHERE {primary_key_column} = %s"
        mycursor.execute(sql, (id,))
        mydb.commit()

        return redirect(url_for('view_data'))

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()


# Route to edit an entry (display form with existing data)
@app.route('/edit/<table>/<int:id>', methods=['GET', 'POST'])
def edit_entry(table, id):
    try:
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)

        if request.method == 'POST':
            # Get updated data from the form
            updated_data = {key: request.form[key] for key in request.form}
            update_query = f"UPDATE {table} SET " + ", ".join([f"{key} = %s" for key in updated_data]) + " WHERE id = %s"
            mycursor.execute(update_query, (*updated_data.values(), id))
            mydb.commit()

            return redirect(url_for('view_data'))
        
        else:
            # Get the current record data to display in the form
            sql = f"SELECT * FROM {table} WHERE id = %s"
            mycursor.execute(sql, (id,))
            record = mycursor.fetchone()

            return render_template('edit_entry.html', table=table, record=record)

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    finally:
        mycursor.close()
        mydb.close()

# Load dataset
data = pd.read_csv('data/healthcare_dataset.csv')

# Data Preprocessing and Analysis
def preprocess_data():
    # Convert date columns to datetime
    data['Date of Admission'] = pd.to_datetime(data['Date of Admission'], errors='coerce')
    data['Discharge Date'] = pd.to_datetime(data['Discharge Date'], errors='coerce')
    
    # Calculate length of stay
    data['Length of Stay'] = (data['Discharge Date'] - data['Date of Admission']).dt.days

    # Summary statistics
    avg_age = data['Age'].mean()
    avg_billing = data['Billing Amount'].mean()
    avg_stay = data['Length of Stay'].mean()
    gender_counts = data['Gender'].value_counts().to_dict()
    blood_type_counts = data['Blood Type'].value_counts().to_dict()

    return {
        'avg_age': avg_age,
        'avg_billing': avg_billing,
        'avg_stay': avg_stay,
        'gender_counts': gender_counts,
        'blood_type_counts': blood_type_counts
    }

# Visualization Functions
def generate_plots():
    # Age distribution histogram
    fig_age = px.histogram(data, x='Age', title='Age Distribution')
    
    # Gender distribution pie chart
    fig_gender = px.pie(data, names='Gender', title='Gender Distribution')
    
    # Blood type distribution pie chart
    fig_blood_type = px.pie(data, names='Blood Type', title='Blood Type Distribution')
    
    # Billing amount box plot
    fig_billing = px.box(data, y='Billing Amount', title='Billing Amount Distribution')
    
    # Admission trend over time
    fig_admission_trend = px.histogram(data, x='Date of Admission', title='Admissions Over Time')
    
    # Return Plotly HTML components
    return {
        'fig_age': fig_age.to_html(full_html=False),
        'fig_gender': fig_gender.to_html(full_html=False),
        'fig_blood_type': fig_blood_type.to_html(full_html=False),
        'fig_billing': fig_billing.to_html(full_html=False),
        'fig_admission_trend': fig_admission_trend.to_html(full_html=False)
    }

@app.route('/analytics')
def analytics():
    # Calculate statistics and plots
    stats = preprocess_data()
    plots = generate_plots()
    return render_template('analytics.html', full_name=session['full_name'], stats=stats, plots=plots)


if __name__ == '__main__':
    app.run(debug=True)

# Example of Data Collection
# When collecting a diagnosis, you might collect the following:

# Symptoms: What the patient is experiencing (e.g., cough, fever).
# Diagnosis: The conclusion made by the healthcare provider (e.g., influenza).
# Disease: The specific disease associated with the diagnosis (e.g., viral influenza).