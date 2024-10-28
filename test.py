from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/register_doctor', methods=['POST'])
def register_doctor():
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="mydatabase"
    )
    
    mycursor = mydb.cursor()
    
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
    
    # Insert doctor data into the database
    sql = """
    INSERT INTO doctors (full_name, email, password, phone, license_number, medical_school, graduation_year,
                         specialization, hospital_affiliation, years_experience, medical_association, reference_contact)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    val = (full_name, email, password, phone, license_number, medical_school, graduation_year, specialization,
           hospital_affiliation, years_experience, medical_association, reference_contact)
    
    mycursor.execute(sql, val)
    mydb.commit()
    
    return "Doctor registration successful!"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to keep session information secure

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="doctor_registration"
    )

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve email and password from the form
        email = request.form['email']
        password = request.form['password']

        # Connect to the database
        mydb = get_db_connection()
        mycursor = mydb.cursor()

        # Fetch the doctor record by email
        mycursor.execute("SELECT doctor_id, password FROM doctors WHERE email = %s", (email,))
        doctor = mycursor.fetchone()

        if doctor:
            doctor_id, hashed_password = doctor
            
            # Check if the password matches the hashed password in the database
            if checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Store doctor_id in session and log them in
                session['doctor_id'] = doctor_id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
        else:
            flash('Email not found.', 'danger')
        
        mycursor.close()
        mydb.close()

    return render_template('login.html')

# Route for the dashboard (after login)
@app.route('/dashboard')
def dashboard():
    # Ensure user is logged in
    if 'doctor_id' in session:
        return "Welcome to the dashboard! You are logged in as doctor_id: " + str(session['doctor_id'])
    else:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('doctor_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/submit_diagnosis', methods=['POST'])
def submit_diagnosis():
    # Connect to the database
    mydb = mysql.connector.connect(
      host="localhost",
      user="yourusername",
      password="yourpassword",
      database="mydatabase"
    )
    
    mycursor = mydb.cursor()
    
    # Retrieve form data
    patient_name = request.form['patient_name']
    age = request.form['age']
    gender = request.form['gender']
    disease_name = request.form['disease']
    diagnosis = request.form['diagnosis']
    test_results = request.form['test_results']
    medications = request.form['medications']
    additional_comments = request.form['additional_comments']
    
    # Retrieve multiple symptoms from the form
    symptoms = [request.form.get(f'symptom_{i}') for i in range(1, 11)]  # Adjust the range based on the number of symptom fields

    # Insert patient information
    sql_patient = "INSERT INTO patients (name, age, gender) VALUES (%s, %s, %s)"
    val_patient = (patient_name, age, gender)
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
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val_diagnosis = (patient_id, disease_id, *symptoms, diagnosis, test_results, medications, additional_comments)
    mycursor.execute(sql_diagnosis, val_diagnosis)

    # Commit the transaction
    mydb.commit()

    return f"Diagnosis for {patient_name} has been recorded successfully!"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
import mysql.connector

app = Flask(__name__)

@app.route('/register_doctor', methods=['POST'])
def register_doctor():
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="mydatabase"
    )
    mycursor = mydb.cursor()

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
from flask import Flask, request, redirect, url_for, render_template, flash, session
from werkzeug.security import check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="mydatabase"
    )

# Route for login page
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
        return f"Welcome to your dashboard, {session['full_name']}!"
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
