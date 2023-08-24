from flask import *
import ibm_db


conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yhr48182;PWD=OvQXer5G7EsykzpF",'','')
print(conn)

app=Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login1',methods=['POST'])
def login1():
    NAME = request.form['NAME']
    EMAIL = request.form['EMAIL']
    sql = "SELECT * FROM REGISTER WHERE NAME =? AND EMAIL=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,NAME)
    ibm_db.bind_param(stmt,2,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(NAME,EMAIL)
    if account:
            return render_template('login.html', pred="Login successful")
    else:
        return render_template('register.html', pred="Login unsuccessful. Please register!") 


@app.route('/register1',methods=['POST'])
def register1():
    x = [x for x in request.form.values()]
    print(x)
    NAME=x[0]
    EMAIL=x[1]
    PASSWORD=x[2]
    sql = "SELECT * FROM REGISTER WHERE EMAIL =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('login.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  REGISTER VALUES (?, ?, ?)"
        prep = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep, 1, NAME)
        ibm_db.bind_param(prep, 2, EMAIL)
        ibm_db.bind_param(prep, 3, PASSWORD)
        ibm_db.execute(prep)
        return render_template('login.html', pred="Registration Successful, please login using your details")


if __name__ == "__main__":
    app.run(debug=True,port = 5000)