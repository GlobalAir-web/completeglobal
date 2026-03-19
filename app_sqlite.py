"""
MongoDB fallback to SQLite
Modify app.py to use SQLite if MongoDB is unavailable
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# ==============================
# APP CONFIG
# ==============================

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "SHASTIKA_ADMIN_PANEL_KEY_2025")

# ==============================
# DATABASE INITIALIZATION (SQLite Fallback)
# ==============================

DB_FILE = "shastika.db"

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create contact_messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create product_enquiries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            name TEXT NOT NULL,
            country TEXT,
            phone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ SQLite Database initialized")

# Initialize database on startup
init_database()

# ==============================
# DATABASE HELPER FUNCTIONS
# ==============================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_contact(name, email, phone, subject, message):
    """Insert contact message"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contact_messages (name, email, phone, subject, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, subject, message))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting contact: {e}")
        return False

def insert_enquiry(product, name, country, phone, email):
    """Insert product enquiry"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO product_enquiries (product, name, country, phone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (product, name, country, phone, email))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting enquiry: {e}")
        return False

def get_all_contacts():
    """Get all contact messages"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC')
        messages = cursor.fetchall()
        conn.close()
        return [dict(m) for m in messages]
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return []

def get_all_enquiries():
    """Get all product enquiries"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM product_enquiries ORDER BY created_at DESC')
        enquiries = cursor.fetchall()
        conn.close()
        return [dict(e) for e in enquiries]
    except Exception as e:
        print(f"Error fetching enquiries: {e}")
        return []

# ==============================
# WEBSITE ROUTES
# ==============================

@app.route("/")
def final():
    return render_template("home.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/countries")
def countries():
    return render_template("countries.html")

@app.route("/awards")
def awards():
    return render_template("awards.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/team")
def team():
    return render_template("team.html")

# ==============================
# API ENDPOINTS
# ==============================

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    """Handle contact form submission"""
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        subject = data.get("subject")
        message = data.get("message")
        
        if insert_contact(name, email, phone, subject, message):
            return jsonify({"status": "success", "message": "Message sent successfully!"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to save message"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/submit_enquiry", methods=["POST"])
def submit_enquiry():
    """Handle product enquiry submission"""
    try:
        data = request.json
        product = data.get("product")
        name = data.get("name")
        country = data.get("country")
        phone = data.get("phone")
        email = data.get("email")
        
        if insert_enquiry(product, name, country, phone, email):
            return jsonify({"status": "success", "message": "Enquiry submitted successfully!"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to save enquiry"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/admin_login", methods=["POST"])
def admin_login():
    """Admin authentication"""
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        
        admin_email = os.getenv("ADMIN_EMAIL", "admin@shastika.com")
        admin_pass = os.getenv("ADMIN_PASS", "Admin@123")
        
        if email == admin_email and password == admin_pass:
            session["admin"] = True
            return jsonify({"status": "success", "message": "Login successful"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/admin/messages", methods=["GET"])
def admin_messages():
    """Get all contact messages (admin only)"""
    if not session.get("admin"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    messages = get_all_contacts()
    return jsonify(messages), 200

@app.route("/admin/enquiries", methods=["GET"])
def admin_enquiries():
    """Get all product enquiries (admin only)"""
    if not session.get("admin"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    enquiries = get_all_enquiries()
    return jsonify(enquiries), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
