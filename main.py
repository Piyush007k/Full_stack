from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

DATABASE = 'Full_Stack_Database.db'
 
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn
 
# Create tables if they do not exist
with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS organization_table
                 (Org_id INTEGER PRIMARY KEY,
                 Org_name TEXT NOT NULL,
                 API_KEY TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS agency_table
                 (Org_id INTEGER,
                 Agency_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                 Agency_name TEXT NOT NULL,
                 Agency_email TEXT NOT NULL,
                 FOREIGN KEY (Org_id) REFERENCES organization_table(Org_id)
                     ON DELETE CASCADE
                     ON UPDATE CASCADE)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS user_table
                 (Org_id INTEGER,
                 Emp_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                 Access_level TEXT NOT NULL,
                 User_name TEXT NOT NULL UNIQUE,
                 Password TEXT NOT NULL,
                 IsAdmin TEXT NOT NULL,
                 Application TEXT NOT NULL,
                 FOREIGN KEY (Org_id) REFERENCES organization_table(Org_id)
                     ON DELETE CASCADE
                     ON UPDATE CASCADE)''')
    
    conn.commit()
 
@app.route('/insert_organization', methods=['POST'])
def insert_organization():
    Org_name = request.form.get('Org_name')
    API_KEY = request.form.get('API_KEY')
    Org_id = request.form.get('Org_id')
    
    if not all([Org_name, API_KEY, Org_id]):
        return jsonify({"error": "Org_name, API_KEY, and Org_id cannot be empty"}), 400
    
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO organization_table (Org_id, Org_name, API_KEY) VALUES (?, ?, ?)", (Org_id, Org_name, API_KEY))
            conn.commit()
        return jsonify({"message": "Inserted into organization_table"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_agency', methods=['POST'])
def insert_agency():
    Org_id = request.form.get('Org_id')
    Agency_name = request.form.get('Agency_name')
    Agency_email = request.form.get('Agency_email')
    
    if not all([Org_id, Agency_name, Agency_email]):
        return jsonify({"error": "Org_id, Agency_name, and Agency_email cannot be empty"}), 400
    
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO agency_table (Org_id, Agency_name, Agency_email) VALUES (?, ?, ?)", (Org_id, Agency_name, Agency_email))
            conn.commit()
        return jsonify({"message": "Inserted into agency_table"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_user', methods=['POST'])
def insert_user():
    Org_id = request.form.get('Org_id')
    Access_level = request.form.get('Access_level')
    User_name = request.form.get('User_name')
    Password = request.form.get('Password')
    IsAdmin = request.form.get('IsAdmin')
    Application = request.form.get('Application')
    
    if not all([Org_id, Access_level, User_name, Password, IsAdmin, Application]):
        return jsonify({"error": "Org_id, Access_level, User_name, Password, IsAdmin, and Application cannot be empty"}), 400
    
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO user_table (Org_id, Access_level, User_name, Password, IsAdmin, Application) VALUES (?, ?, ?, ?, ?, ?)", (Org_id, Access_level, User_name, Password, IsAdmin, Application))
            conn.commit()
        return jsonify({"message": "Inserted into user_table"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/select_user_by_credentials', methods=['POST'])
def select_user_by_credentials():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not all([username, password]):
        return jsonify({"error": "Username and password cannot be empty"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_table WHERE User_name = ? AND Password = ?", (username, password))
        rows = cursor.fetchall()
        conn.close()
        users = []
        for row in rows:
            user = dict(row)
            users.append(user)
        if users:
            return jsonify({"users": users}), 200
        else:
            return jsonify({"message": "No user found with provided credentials"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/update_user', methods=['POST'])
def update_user():
    Org_id = request.form.get('Org_id')
    User_name = request.form.get('User_name')
    new_Access_level = request.form.get('new_Access_level')
    new_Password = request.form.get('new_Password')
    new_IsAdmin = request.form.get('new_IsAdmin')
    new_Application = request.form.get('new_Application')
    
    # Check if any required fields are empty
    if not all([Org_id, User_name]):
        return jsonify({"error": "Org_id and User_name cannot be empty"}), 400
    
    try:
        with get_db_connection() as conn:
            # Check if the user exists
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_table WHERE Org_id = ? AND User_name = ?", (Org_id, User_name))
            user = cursor.fetchone()
            if user:
                # Update user details if new values are provided
                updates = []
                if new_Access_level:
                    updates.append(("Access_level", new_Access_level))
                if new_Password:
                    updates.append(("Password", new_Password))
                if new_IsAdmin:
                    updates.append(("IsAdmin", new_IsAdmin))
                if new_Application:
                    updates.append(("Application", new_Application))
                
                # Construct and execute the update query
                if updates:
                    update_query = "UPDATE user_table SET " + ", ".join(f"{col} = ?" for col, _ in updates) + " WHERE Org_id = ? AND User_name = ?"
                    update_values = [val for _, val in updates] + [Org_id, User_name]
                    conn.execute(update_query, update_values)
                    conn.commit()
                    return jsonify({"message": "User details updated successfully"}), 200
                else:
                    return jsonify({"message": "No updates provided"}), 200
            else:
                return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
from flask import jsonify

@app.route('/view_users', methods=['POST'])
def view_users_route():
    Org_id = request.form.get('Org_id')
    User_name = request.form.get('User_name')
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Access_level FROM user_table WHERE Org_id = ? AND User_name = ?", (Org_id, User_name))
            user = cursor.fetchone()
            if user:
                access_level = user['Access_level']
                if access_level == 'superuser':  # Superuser
                    cursor.execute("SELECT * FROM user_table")
                else:  # Normal user
                    cursor.execute("SELECT * FROM user_table WHERE Org_id = ?", (Org_id,))
                rows = cursor.fetchall()
                users = [dict(row) for row in rows]
                return jsonify({"users": users}), 200
            else:
                return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/delete_user', methods=['POST'])
def delete_user():
    User_name = request.form.get('User_name')
    
    if not User_name:
        return jsonify({"error": "User_name cannot be empty"}), 400
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_table WHERE User_name = ?", (User_name,))
            user = cursor.fetchone()
            if user:
                cursor.execute("DELETE FROM user_table WHERE User_name = ?", (User_name,))
                conn.commit()
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
if __name__ == '__main__':
    app.run(host = "0.0.0.0",port = '5000', debug=True)