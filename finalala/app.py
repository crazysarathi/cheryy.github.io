# from urllib import request
from flask import Flask, render_template, request
# for ibm
import ibm_db
conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=31864; SECURITY=SSL;UID=lzb30139;PWD=hcstv3ifonoHbliD", '', '')
# end of ibm

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('register.html')
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    
    
    # insert the data into the table
    stmt = ibm_db.prepare(conn, "INSERT INTO USERS (EMAIL, PASSWORD) VALUES (?, ?)")
    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, email)

    ibm_db.execute(stmt)
    
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        stmt = ibm_db.prepare(conn, "SELECT * FROM USERS WHERE EMAIL = ?")
        ibm_db.bind_param(stmt, 1, email)
        result = ibm_db.execute(stmt)
        row = ibm_db.fetch_assoc(result)
    
        if row:
            return render_template('simple.html')
        else:
            error = 'Invalid email address. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)