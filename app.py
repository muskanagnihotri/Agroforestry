from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask import flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            field_photo TEXT,
            plot_location TEXT,
            tree_species TEXT,
            created_by TEXT NOT NULL,
            reported_to TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Dummy user data
users = {
    'exec_a': {'password': 'pass_a', 'role': 'Field Executive'},
    'exec_b': {'password': 'pass_b', 'role': 'Field Executive'},
    'mgr_c': {'password': 'pass_c', 'role': 'Field Manager'},
    'mgr_d': {'password': 'pass_d', 'role': 'Field Manager'},
    'senior_mgr': {'password': 'pass_e', 'role': 'Senior Manager'}
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']

            if session['role'] == 'Field Executive':
                return redirect(url_for('add_farm_data'))
        
            return redirect(url_for('dashboard'))     
        return "Invalid username or password!"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        role = session.get('role')
        username = session.get('username')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if role == 'Senior Manager':
            cursor.execute("SELECT * FROM farmers")
        elif role == 'Field Manager':
            cursor.execute("SELECT * FROM farmers WHERE reported_to = ?", (username,))
        else:
            return "Field Executives cannot view the dashboard!"

        farmers = cursor.fetchall()
        conn.close()

        return render_template('dashboard.html', farmers=farmers, role=role)
    return redirect(url_for('login'))


@app.route('/add_farm_data', methods=['GET', 'POST'])
def add_farm_data():
    if 'username' in session and session.get('role') == 'Field Executive':
        if request.method == 'POST':
            # Retrieve form data
            farmer_name = request.form.get('farmer_name', '').strip()
            contact_number = request.form.get('contact_number', '').strip()
            field_photo = request.form.get('field_photo', '').strip()
            plot_location = request.form.get('plot_location', '').strip()
            tree_species = request.form.get('tree_species', '').strip()
            reported_to = request.form.get('reported_to', '').strip()  # Added field
            created_by = session.get('username')

            # Validate input fields
            if not farmer_name or not contact_number or not plot_location or not tree_species or not reported_to:
                flash("All required fields must be filled!", "error")
                return redirect(url_for('add_farm_data'))

            try:
                # Save data into the database
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO farmers (farmer_name, contact_number, field_photo, plot_location, tree_species, created_by, reported_to)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (farmer_name, contact_number, field_photo, plot_location, tree_species, created_by, reported_to))
                conn.commit()
                conn.close()

                flash("Data added successfully!", "success")
                return redirect(url_for('add_farm_data'))
            except Exception as e:
                flash(f"An error occurred while saving data: {e}", "error")
                return redirect(url_for('add_farm_data'))

        return render_template('farmer_form.html')
    return redirect(url_for('login'))


@app.route('/update_farm_data/<int:id>', methods=['GET', 'POST'])
def update_farm_data(id):
    if 'username' in session and session.get('role') == 'Senior Manager':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if request.method == 'POST':
            farmer_name = request.form['farmer_name']
            contact_number = request.form['contact_number']
            field_photo = request.form['field_photo']
            plot_location = request.form['plot_location']
            tree_species = request.form['tree_species']

            try:
                cursor.execute('''
                    UPDATE farmers
                    SET farmer_name = ?, contact_number = ?, field_photo = ?, plot_location = ?, tree_species = ?
                    WHERE id = ?
                ''', (farmer_name, contact_number, field_photo, plot_location, tree_species, id))
                conn.commit()
                flash("Data updated successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "error")
            finally:
                conn.close()
                return redirect(url_for('dashboard'))

        cursor.execute("SELECT * FROM farmers WHERE id = ?", (id,))
        farmer = cursor.fetchone()
        conn.close()

        return render_template('update_form.html', farmer=farmer)
    return redirect(url_for('login'))


@app.route('/delete_farm_data/<int:id>', methods=['GET'])
def delete_farm_data(id):
    if session.get('role') == 'Senior Manager':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM farmers WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
