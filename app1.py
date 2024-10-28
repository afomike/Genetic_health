
from flask import Flask, render_template, request, session, redirect, url_for,g
import os 
import pandas as pd
import MySQLdb as mysqlclient
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import shutil
import numpy as np

app = Flask(__name__)
# # app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
# app.secret_key = 'my_super_secret_key_123456789'
# # Database configuration pythonanywhere 
# host = 'magratedata.mysql.pythonanywhere-services.com'
# database = 'magratedata$magratedb'
# user = 'magratedata'
# password = 'afo@@1234MIKE'

# # Establish a connection
# mysql = MySQLdb.connect(host=host, user=user, password=password, db=database)

# # Create a cursor object to interact with the database
# cursor = mysql.cursor()


# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'magratedb'

# # Function to get the database connection
# def get_db():
#     return mysqlclient.connect(host=app.config['MYSQL_HOST'],
#                         user=app.config['MYSQL_USER'],
#                         password=app.config['MYSQL_PASSWORD'],
#                         db=app.config['MYSQL_DB'])

# Function to get a cursor from the database connection
def get_cursor():
    return get_db().cursor()
# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = mysqlclient.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        password=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'])

    return g.db

# Function to get a cursor from the database connection
def get_cursor():
    return get_db().cursor()

# Function to close the database connection
@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

clinical_departments_list = [
    "Casualty department","Operating theatre (OT)","Intensive care unit (ICU)",
    "Anesthesiology department","Cardiology department","Ear and Throat (ENT) department",
    "Geriatric department","Gastroenterology department","General surgery",
    "Gynaecology department","Haematology department","Pediatrics department",
    "Neurology department","Oncology department","Opthalmology department",
    "Orthopaedic department","Urology department","Psychiatry department",
    "Inpatient Department (IPD)","Outpatient Department (OPD)","Nursing Department"
]

supportive_departments_list = [
    "Pharmacy department","Radiology department","Clinical pathology department",
    "Nutrition and dietetics","Catering and food services","Central sterilization unit",
    "Housekeeping"
]

technical_departments_list = [
    "Clinical engineering department","Information technology and communication","Engineering Services"
]

administrative_departments_list = [
    "Medical records department","Human resources department","Finance department",
    "Administrative department"
]

# # Function to get the database connection
# def get_db():
#     if 'db' not in g:
#         g.db = mysqlclient.connect(host=host, user=user, password=password, db=database)
#     return g.db

# # Function to get a cursor from the database connection
# def get_cursor():
#     return get_db().cursor()

# # Function to close the database connection
# @app.teardown_appcontext
# def close_db(error):
#     if 'db' in g:
#         g.db.close()

# ... (other parts of your code)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', setlogin="login")

    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        cursor = get_cursor()
        cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
        user_data = cursor.fetchone()

        if user_data and check_password_hash(user_data[1], password):
            session['username'] = user_data[0]
            session['department'] = user_data[3]
            session['name'] = user_data[4]
            return redirect(url_for('dashboard'))
        else:
            alert_script = "<script>alert('Invalid username or password');</script>"
            return f"{alert_script}<script>window.location.href = '{url_for('index')}';</script>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        setreg = "reg"
        return render_template('index.html', clinical_departments=clinical_departments_list,
                               supportive_departments=supportive_departments_list,
                               technical_departments=technical_departments_list,
                               administrative_departments=administrative_departments_list, setreg=setreg)

    if request.method == 'POST':
        username = request.form.get('Username')
        raw_password = request.form.get('Password')

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(raw_password, method='sha256')

        Firstname = request.form.get('Firstname')
        Middlename = request.form.get('Middlename')
        Lastname = request.form.get('Lastname')
        Name = f'{Firstname} {Middlename} {Lastname}'
        Email = request.form.get('Email')
        phone = request.form.get('phone')
        department_type = request.form.get('department_type')

        cursor = get_cursor()
        cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            alert_script = "<script>alert('Username already exists. Choose a different username.');</script>"
            return f"{alert_script}<script>window.location.href = '{url_for('index')}';</script>"
        else:
            cursor.execute("INSERT INTO user (username, password, department, Name, Email, Phonenumber) VALUES (%s, %s, %s, %s, %s, %s)",
                            (username, hashed_password, department_type, Name, Email, phone))
            get_db().commit()

            alert_script = "<script>alert('Account Created Successfully ');</script>"
            return f"{alert_script}<script>window.location.href = '{url_for('index')}';</script>"

    
@app.route('/dashboard', methods=['GET', 'POST'])   
def dashboard():
    if 'username' in session:
        # return render_template('dashboard.html')
        # return f"Welcome, {session['username']}!"
        department= session['department'] 
        name= session['name'] 
        root_folder ='Data'
        tree_structure = folderview(root_folder)

        return render_template('dashboard.html',tree_structure=tree_structure,initial_depth=3,
                               department=department,name=name)
    else:
        return redirect(url_for('index'))
@app.route('/format', methods=['GET', 'POST'])   
def format():
    if 'username' in session:
        # return render_template('dashboard.html')
        # return f"Welcome, {session['username']}!"
        department= session['department'] 
        name= session['name'] 
        root_folder ='Data2'
        tree_structure = folderview(root_folder)

        return render_template('dashboard.html',tree_structure=tree_structure,initial_depth=9,
                               department=department,name=name)
    else:
        return redirect(url_for('index'))
def folderview(root_folder):
    # root_folder = root_folder
    tree_structure = generate_tree_structure(root_folder)
    # Pass the initial depth to the template
    # return render_template('dashboard.html', tree_structure=tree_structure, initial_depth=3)
    return tree_structure





@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))
    app.config['UPLOAD_FOLDER'] = 'Data'
    # request.form['Age']
    department_to_check = session['department']

    
    if department_to_check in clinical_departments_list:
        subfolder = f'Clinical_Departments_in_a_Hospital/{department_to_check}'
        print(f"{department_to_check} is a Clinical Department.")
    elif department_to_check in supportive_departments_list:
        subfolder = f'Supportive_Departments_in_a_Hospital/{department_to_check}'
        print(f"{department_to_check} is a Supportive Department.")
    elif department_to_check in technical_departments_list:
        subfolder = f'Technical_Departments_in_a_Hospital/{department_to_check}'
        print(f"{department_to_check} is a Technical Department.")
    elif department_to_check in administrative_departments_list:
        subfolder = f'Administrative_Departments_in_a_Hospital/{department_to_check}'
        print(f"{department_to_check} is an Administrative Department.")
    else:
        print(f"{department_to_check} is not in either Clinical, Supportive, Technical, or Administrative Departments.")

    # subfolder = 'Clinical_Departments_in_a_Hospital/dsis'
    # app.config['UPLOAD_FOLDER'] = 'Data'
    
    file = request.files['file']

    if file:
        global subfolder_path 
        subfolder_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        upload_path = os.path.join(subfolder_path, secure_filename(file.filename))
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        file.save(upload_path)
        CallSortbyMl(subfolder_path,subfolder)
        # return 'File uploaded successfully.'
        alert_script = "<script>alert('File uploaded successfully.');</script>"
        return f"{alert_script}<script>window.location.href = '{url_for('dashboard')}';</script>"
        
    # return 'No file selected.'
    alert_script = "<script>alert('No file selected. ');</script>"
    return f"{alert_script}<script>window.location.href = '{url_for('dashboard')}';</script>"
# @app.route('/view')
# def view():
#     root_folder = 'Data'
#     tree_structure = generate_tree_structure(root_folder)
#     # Pass the initial depth to the template
#     return render_template('view.html', tree_structure=tree_structure, initial_depth=3)

def generate_tree_structure(root_folder):
    tree_structure = {'name': root_folder, 'type': 'folder', 'children': []}
    populate_tree(root_folder, tree_structure)
    return tree_structure

def populate_tree(folder_path, node):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        child_node = {'name': item, 'type': 'folder' if os.path.isdir(item_path) else 'file', 'children': []}
        node['children'].append(child_node)
        if os.path.isdir(item_path):
            populate_tree(item_path, child_node)


# Define the folders
folders = ["Images", "Documents", "Records", "Other"]

# Initialize Q-table with zeros
q_table = {(folder, file_type): 0 for folder in folders for file_type in folders}

# Define the learning rate, discount factor, and exploration rate
alpha_initial = 0.5  # Initial learning rate
alpha = alpha_initial  # Current learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate

def get_file_type(filename):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return "Images"
    elif filename.lower().endswith(('.doc', '.docx', '.pdf', '.txt')):
        return "Documents"
    elif filename.lower().endswith(('.csv', '.xlsx', '.db')):
        return "Records"
    else:
        return "Other"

def choose_folder(file_type):
    # Use epsilon-greedy strategy for exploration
    if epsilon > 0.1 and np.random.rand() < epsilon:
        return np.random.choice(folders)
    else:
        # Choose folder with the highest Q-value for the given file type
        max_q_value = max(q_table[(folder, file_type)] for folder in folders)
        best_folders = [folder for folder in folders if q_table[(folder, file_type)] == max_q_value]
        return np.random.choice(best_folders)

def update_q_table(folder, file_type, reward):
    # Update Q-value based on the reward
    old_q_value = q_table[(folder, file_type)]
    best_next_q_value = max(q_table[(next_folder, file_type)] for next_folder in folders)
    new_q_value = old_q_value + alpha * (reward + gamma * best_next_q_value - old_q_value)
    q_table[(folder, file_type)] = new_q_value

def organize_files(source_folder, destination_folder):
    # Remove existing destination folder to override it
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)

    # Recreate destination folders
    for folder in folders:
        folder_path = os.path.join(destination_folder, folder)
        os.makedirs(folder_path, exist_ok=True)

    files_found = False  # Flag to track if any files are found in the source folder

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path):
            files_found = True  # Set the flag to True as at least one file is found
            file_type = get_file_type(filename)
            folder = choose_folder(file_type)

            # For simplicity, assume a positive reward for successful organization
            reward = 0.6

            # Save the file to the assigned folder
            save_file(file_path, os.path.join(destination_folder, folder, filename))

            # Update Q-table
            update_q_table(folder, file_type, reward)

    if not files_found:
        print("No files found in the source folder.")

def save_file(source_path, destination_path):
    # Implement your file-saving logic here (e.g., move or copy the file)
    shutil.copy(source_path, destination_path)
    
# def consolidate_files(destination_folder):
#     for filename in os.listdir(destination_folder):
#         file_path = os.path.join(destination_folder, filename)
#         if os.path.isfile(file_path):
#             file_type = get_file_type(filename)
#             folder = choose_folder(file_type)

#             # Move the file back to the chosen folder
#             save_file(file_path, os.path.join(destination_folder, folder, filename))

#             # Update Q-table during consolidation
#             reward = 1
#             update_q_table(folder, file_type, reward)
def CallSortbyMl(source_folder, destination_folder_name):
    destination_folder = f"Data2/{destination_folder_name}"
    # destination_folder = os.path.join(folder1, destination_folder_name)
    # os.makedirs(destination_folder, exist_ok=True)
    # Run the main training loop with Q-learning
    num_iterations = 1

    for _ in range(num_iterations):
        organize_files(source_folder, destination_folder)


        # After the loop, call the consolidate_files function
        # consolidate_files(destination_folder)

        # Display the final Q-table
    print("\nFinal Q-table:")
    for key, value in q_table.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    # app.secret_key = os.urandom(12).hex()
    key = secrets.token_hex(16)  # Generates a 32-character random hexadecimal string
    app.secret_key = key
    app.run(debug=True)



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

# Create the database
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
