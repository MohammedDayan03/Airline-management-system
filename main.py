from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from functools import wraps

app = Flask(__name__)
app.secret_key = 'airline_dbms_secret_key_2026'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MdDayan@7',
    'database': 'airline_dbms'
}

# Function to connect to database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as err:
        print(f"Error: {err}")
        return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===== Authentication Routes =====
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                cursor.close()
                if user:
                    session['user'] = username
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html', error='Invalid credentials')
            except Error as err:
                print(f"Error: {err}")
                return render_template('login.html', error='Database error')
            finally:
                connection.close()
        else:
            return render_template('login.html', error='Database connection failed')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, 'passenger')", (username, password, email))
                connection.commit()
                cursor.close()
                return redirect(url_for('login'))
            except Error as err:
                print(f"Error: {err}")
                return render_template('signup.html', error='Username already exists or error occurred')
            finally:
                connection.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ===== CUSTOMER Routes =====
@app.route('/home')
@login_required
def home():
    return render_template('index.html', user=session.get('user'))

@app.route('/flights')
@login_required
def flights():
    return render_template('flights.html', user=session.get('user'))

@app.route('/about')
@login_required
def about():
    return render_template('about.html', user=session.get('user'))

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html', user=session.get('user'))

@app.route('/faq')
@login_required
def faq():
    return render_template('faq.html', user=session.get('user'))

@app.route('/offers')
@login_required
def offers():
    return render_template('offers.html', user=session.get('user'))

@app.route('/miles')
@login_required
def miles():
    return render_template('miles.html', user=session.get('user'))

@app.route('/bookings')
@login_required
def bookings():
    return render_template('bookings.html', user=session.get('user'))

if __name__ == '__main__':
    app.run(debug=True)