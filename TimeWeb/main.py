from flask import Flask, abort, request, render_template, send_file, redirect, url_for
import sqlite3
import random

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

@app.route('/download_file/<filename>')
def download_file(filename):
    file_options = ['files\выписка_некоррект.pdf', 'files\выписка.pdf']
    file_to_download = random.choice(file_options)

    return send_file(file_to_download, as_attachment=True, download_name=filename+'.pdf')

if __name__ == "__main__":
    app.run()