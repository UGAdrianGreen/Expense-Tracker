from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        amount REAL,
                        date TEXT
                    )''')
    conn.commit()
    return conn

# Route for the home page
@app.route('/')
def index():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=data)

# Route to add an expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    date = request.form['date']
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)', (category, amount, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
