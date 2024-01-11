from flask import Flask, abort, request, render_template, send_file, redirect, url_for, json, jsonify
import sqlite3
import random
import requests

app = Flask(__name__)

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT password FROM passwords
                                                WHERE login = '{}';
                                                ''').format(Login))
        pas = cursor_db.fetchall()

        cursor_db.close()
        try:
            if pas[0][0] != Password:
                return render_template('auth_bad.html')
        except:
            return render_template('auth_bad.html')

        
        db_lp.close()

        error = random.choice(range(2))
        if error > 0:
            abort(400, 'Record not found') 
        return redirect(url_for('download_file', filename=Login))
    

    return render_template('authorization.html')

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():

    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, Password)


        cursor_db.execute(sql_insert)

        cursor_db.close()

        db_lp.commit()
        db_lp.close()

        return render_template('successfulregis.html')

    return render_template('registration.html')

@app.route('/createcase', methods=['GET', 'POST'])
def form_create_case():

    if request.method == 'POST':
        credit_program = request.form.get('creditProgram')
        loan_amount = request.form.get('loanAmount')
        loan_period = request.form.get('loanPeriod')
        last_name = request.form.get('lastName')
        first_name = request.form.get('firstName')
        middle_name = request.form.get('middleName')
        dob = request.form.get('dob')
        passport_series = request.form.get('passportSeries')
        passport_number = request.form.get('passportNumber')
        passport_issue_date = request.form.get('passportIssueDate')
        passport_issued_by = request.form.get('passportIssuedBy')
        snils = request.form.get('snils')
        education = request.form.get('education')
        registration_address = request.form.get('registrationAddress')
        residential_address = request.form.get('residentialAddress')
        phone = request.form.get('phone')
        agreement = request.form.get('agreement')

        # Формирование JSON-объекта
        form_data = {
            'credit_program': credit_program,
            'loan_amount': loan_amount,
            'loan_period': loan_period,
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'dob': dob,
            'passport_series': passport_series,
            'passport_number': passport_number,
            'passport_issue_date': passport_issue_date,
            'passport_issued_by': passport_issued_by,
            'snils': snils,
            'education': education,
            'registration_address': registration_address,
            'residential_address': residential_address,
            'phone': phone,
            'agreement': agreement
        }

        send_data_to_server(form_data)

        response_data = {
            'status': 'success',
            'message': 'Заявка успешно создана'
        }

        return jsonify(response_data)

    return render_template('loan_ankt.html')

@app.route('/create_loan_case', methods=['GET', 'POST'])
def create_loan_case():
    try:
        response_data = {
                'status': 'success',
                'message': 'Данные успешно получены и обработаны'
            }
        return jsonify(response_data)
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': str(e),
            'data': None
        }
        return jsonify(error_response)

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        response_data = {
                'status': 'success',
                'message': 'Вход успешно совершен'
            }
        return jsonify(response_data)
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': str(e),
            'data': None
        }
        return jsonify(error_response)

@app.route('/getinfo', methods=['GET', 'POST'])
def get_info():
    try:
        response_data = {
                'status': 'success',
                'message': 'Данные успешно загружены'
            }
        return jsonify(response_data)
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': str(e),
            'data': None
        }
        return jsonify(error_response)
    
def send_data_to_server(data):
    server_url = 'http://127.0.0.1:5000/create_loan_case'

    requests.post(server_url, json=data)

@app.route('/download_file/<filename>')
def download_file(filename):
    file_options = ['files\выписка_некоррект.pdf', 'files\выписка.pdf']
    file_to_download = random.choice(file_options)

    return send_file(file_to_download, as_attachment=True, download_name=filename+'.pdf')

if __name__ == "__main__":
    app.run()
