from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PRA#23kgrw9'
app.config['MYSQL_DB'] = 'hrms_database'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files

mysql = MySQL(app)

# Configure a secret key for flash messages (required for flashing error/success messages)
app.secret_key = 'your_secret_key'

# Create the uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Define routes and views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invite', methods=['GET', 'POST'])
def invite():
    if request.method == 'POST':
        # Retrieve form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        course_name = request.form['course_name']
        course_timing = request.form['course_timing']
        nationality = request.form['nationality']
        enrollment_id = request.form['enrollment_id']

        # Upload payment receipt file
        if 'payment_receipt' in request.files:
            payment_receipt = request.files['payment_receipt']
            payment_receipt_path = os.path.join(app.config['UPLOAD_FOLDER'], payment_receipt.filename)
            payment_receipt.save(payment_receipt_path)
        else:
            payment_receipt_path = None

        # Insert data into the database
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO student_invitations (firstname, lastname, phone, email, course_name, course_timing, "
            "payment_receipt, nationality, enrollment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (firstname, lastname, phone, email, course_name, course_timing, payment_receipt_path, nationality, enrollment_id)
        )
        mysql.connection.commit()
        cur.close()

        flash('Invitation sent successfully', 'success')
        return redirect(url_for('invite'))

    return render_template('invite.html')

if __name__ == '__main__':
    app.run(debug=True)
