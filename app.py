from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session and flash messages

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sovit',  
    'database': 'assessment_portal'
}

def init_db():
    """Initialize database and tables if they don't exist."""
    try:
        # Connect without database first to create it
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        conn.database = db_config['database']
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create demo_requests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS demo_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create assessments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                duration INT NOT NULL,
                total_marks INT NOT NULL,
                start_date DATETIME,
                end_date DATETIME,
                status ENUM('draft', 'published') DEFAULT 'draft',
                created_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)

        # Create questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                assessment_id INT NOT NULL,
                question_text TEXT NOT NULL,
                option_a VARCHAR(255) NOT NULL,
                option_b VARCHAR(255) NOT NULL,
                option_c VARCHAR(255) NOT NULL,
                option_d VARCHAR(255) NOT NULL,
                correct_option CHAR(1) NOT NULL,
                FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
            )
        """)
        
        # Create default admin user if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
            conn.commit()
            print("Default user 'admin' created with password 'password123'")
            
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")

# Initialize DB on startup
init_db()

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Database connection failed', 'error')
            
    return render_template('login.html')

@app.route('/book-demo', methods=['POST'])
def book_demo():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO demo_requests (name, email, phone, message) VALUES (%s, %s, %s, %s)',
                (name, email, phone, message)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Demo request submitted successfully! We will contact you soon.', 'success')
        except mysql.connector.Error as err:
            print(f"Error inserting demo request: {err}")
            flash('An error occurred while submitting your request.', 'error')
    else:
        flash('Database connection failed', 'error')
        
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access the dashboard', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/create-test', methods=['POST'])
def create_test():
    if 'user_id' not in session:
        return {'success': False, 'message': 'Unauthorized'}, 401
    
    try:
        data = request.json
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Insert Assessment
            cursor.execute("""
                INSERT INTO assessments (title, description, duration, total_marks, start_date, end_date, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data['title'],
                data['description'],
                data['duration'],
                data['total_marks'],
                data['start_date'],
                data['end_date'],
                session['user_id']
            ))
            assessment_id = cursor.lastrowid
            
            # Insert Questions
            for q in data['questions']:
                cursor.execute("""
                    INSERT INTO questions (assessment_id, question_text, option_a, option_b, option_c, option_d, correct_option)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    assessment_id,
                    q['question_text'],
                    q['option_a'],
                    q['option_b'],
                    q['option_c'],
                    q['option_d'],
                    q['correct_option']
                ))
            
            conn.commit()
            cursor.close()
            conn.close()
            return {'success': True, 'message': 'Assessment created successfully!'}
        else:
            return {'success': False, 'message': 'Database connection failed'}, 500
            
    except Exception as e:
        print(f"Error creating test: {e}")
        return {'success': False, 'message': str(e)}, 500

@app.route('/manage-assessments')
def manage_assessments():
    if 'user_id' not in session:
        return {'success': False, 'message': 'Unauthorized'}, 401
        
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, start_date, duration, status 
            FROM assessments 
            WHERE created_by = %s 
            ORDER BY created_at DESC
        """, (session['user_id'],))
        assessments = cursor.fetchall()
        cursor.close()
        conn.close()
        return {'success': True, 'assessments': assessments}
    return {'success': False, 'message': 'Database connection failed'}, 500

@app.route('/assessment/<int:id>/<action>', methods=['POST'])
def assessment_action(id, action):
    if 'user_id' not in session:
        return {'success': False, 'message': 'Unauthorized'}, 401
        
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # Verify ownership
        cursor.execute("SELECT id FROM assessments WHERE id = %s AND created_by = %s", (id, session['user_id']))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {'success': False, 'message': 'Assessment not found or unauthorized'}, 404
            
        if action == 'delete':
            cursor.execute("DELETE FROM assessments WHERE id = %s", (id,))
        elif action == 'publish':
            cursor.execute("UPDATE assessments SET status = 'published' WHERE id = %s", (id,))
        elif action == 'unpublish':
            cursor.execute("UPDATE assessments SET status = 'draft' WHERE id = %s", (id,))
            
        conn.commit()
        cursor.close()
        conn.close()
        return {'success': True, 'message': f'Assessment {action}d successfully'}
        
    return {'success': False, 'message': 'Database connection failed'}, 500

if __name__ == '__main__':
    app.run(debug=True)
