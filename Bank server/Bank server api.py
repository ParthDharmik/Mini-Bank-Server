from flask import Flask, render_template, request, url_for, redirect, session
import psycopg2

app = Flask(__name__)

app.secret_key = "i-wanna-kms"

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="10001",
        database="personal_db",
        user="postgres",
        password="2007"
    )

@app.route('/')
def home():
    return render_template('Front page.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    error = None

    if request.method == 'POST':
        Account_number = request.form.get('account_number')
        Password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT password FROM accounts WHERE account_no = %s", (Account_number,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result is None:
            error = "Username not found"
        elif result[0].strip() != Password:
            error = "Wrong password"
        else:
            session["s_acc_no"] = Account_number
            return redirect(url_for("user_dashboard"))

    return render_template('Users login.html', error=error)


@app.route('/users/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    error = None
    
    if "s_acc_no" not in session:
        return redirect(url_for("users"))
    
    Account_number = session["s_acc_no"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT balance FROM accounts WHERE account_no = %s",(Account_number,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is None:
        balance = 0
    else:
        balance = result[0]

    if request.method == 'POST':
        to_account = request.form.get('account_number')
        try:
            amount = float(request.form.get('amount'))
        except:
            return redirect(url_for("user_dashboard"))
        
        if amount<=0:
            error = "Amount must be positive"
        elif amount>balance:
            error = "Insufficient balance"
        else:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM accounts WHERE account_no=%s",(to_account,))
            
            if cur.fetchone() is None:
                error = "Receiver account does not exist"

            else:

                cur.execute("UPDATE accounts " \
                            "SET balance=balance-%s " \
                            "WHERE account_no=%s", (amount, Account_number))
                
                cur.execute("UPDATE accounts " \
                            "SET balance=balance+%s " \
                            "WHERE account_no=%s", (amount, to_account))
                conn.commit()
            
            cur.execute("SELECT balance FROM accounts WHERE account_no=%s",(Account_number,))
            balance = cur.fetchone()[0] 

            cur.close()
            conn.close()

    return render_template("Users dashboard.html", balance_html=balance, error=error)

@app.route('/employees',methods=['GET', 'POST'])
def employees():
    error = None
    if request.method == 'POST':
        Id = request.form.get('id')
        Password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT password FROM employees WHERE id = %s", (Id,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result is None:
            error = "Username not found"
        elif result[0].strip() != Password:
            error = "Wrong password"
        else:
            session["s_id"] = Id
            return redirect(url_for("employee_dashboard"))

    return render_template('Employees login.html', error=error)

@app.route('/employees/dashboard', methods=['GET', 'POST'])
def employee_dashboard():

    error = None
    if "s_id" not in session:
        return redirect(url_for("employees"))

    if request.method == 'POST':
        to_account = request.form.get('account_number')
        try:
            amount = float(request.form.get('amount'))
        except:
            return redirect(url_for("employee_dashboard"))
        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM accounts WHERE account_no=%s",(to_account,))
        
        if cur.fetchone() is None:
            error = "Receiver account does not exist"

        else:
            cur.execute("UPDATE accounts " \
                        "SET balance=%s " \
                        "WHERE account_no=%s", (amount, to_account))
            conn.commit()

        cur.close()
        conn.close()

    return render_template("Employees dashboard.html",error=error)

if __name__ == '__main__':
    app.run(debug=True)
