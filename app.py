from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
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
# DATABASE CONFIGURATION
# ==============================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://itsolutions_db_user:S2pMMid2iJQ9MnZv@cluster0.mzaa2iz.mongodb.net/?appName=Cluster0"
)

DB_FILE = "shastika.db"
USE_MONGODB = True

client = None
db = None
contact_collection = None
enquiry_collection = None

# ==============================
# SQLITE INITIALIZATION
# ==============================

def init_sqlite_db():
    """Initialize SQLite database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
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
        print("✓ SQLite database initialized")
        return True
    except Exception as e:
        print(f"✗ Error initializing SQLite: {e}")
        return False

def get_sqlite_db():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ==============================
# MONGODB CONNECTION
# ==============================

def connect_to_mongodb():
    """Initialize MongoDB connection"""
    global client, db, contact_collection, enquiry_collection, USE_MONGODB
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5001)
        # Verify connection
        client.admin.command('ping')
        db = client["shastikaDB"]
        
        contact_collection = db["contact_messages"]
        enquiry_collection = db["product_enquiries"]
        
        USE_MONGODB = True
        print("✓ MongoDB connected successfully")
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("  → Switching to SQLite fallback")
        USE_MONGODB = False
        return False
    except Exception as e:
        print(f"✗ Unexpected error connecting to MongoDB: {e}")
        print("  → Switching to SQLite fallback")
        USE_MONGODB = False
        return False

# Initialize databases on startup
print("\n" + "="*50)
print("DATABASE INITIALIZATION")
print("="*50)
connect_to_mongodb()
if not USE_MONGODB:
    init_sqlite_db()
print("="*50 + "\n")
# ==============================
# WEBSITE HOME
# ==============================

@app.route("/")
def final():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

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

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/location")
def location():
    return render_template("location.html")
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/objectives")
def objectives():
    return render_template("objectives.html")


# ==============================
# DYNAMIC PRODUCT PAGES
# ==============================

@app.route("/product/<product_name>")
def product_page(product_name):
    try:
        return render_template(f"products/{product_name}.html")
    except Exception as e:
        print(f"Error loading product page '{product_name}': {e}")
        import traceback
        traceback.print_exc()
        abort(404)

# ==============================
# CONTACT FORM API
# ==============================

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        subject = data.get("subject")
        message = data.get("message")
        
        if USE_MONGODB and contact_collection:
            contact_collection.insert_one({
                "name": name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message
            })
        else:
            conn = get_sqlite_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contact_messages (name, email, phone, subject, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, subject, message))
            conn.commit()
            conn.close()
        
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error inserting contact: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ==============================
# PRODUCT ENQUIRY API
# ==============================

@app.route("/submit_enquiry", methods=["POST"])
def submit_enquiry():
    try:
        data = request.json
        product = data.get("product")
        name = data.get("name")
        country = data.get("country")
        phone = data.get("phone")
        email = data.get("email")
        
        if USE_MONGODB and enquiry_collection:
            enquiry_collection.insert_one({
                "product": product,
                "name": name,
                "country": country,
                "phone": phone,
                "email": email
            })
        else:
            conn = get_sqlite_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO product_enquiries (product, name, country, phone, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (product, name, country, phone, email))
            conn.commit()
            conn.close()
        
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error inserting enquiry: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ==============================
# ADMIN LOGIN
# ==============================

@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@shastika.com")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "Admin@123")

    if data.get("email") == ADMIN_EMAIL and data.get("password") == ADMIN_PASS:
        session["admin"] = True
        return jsonify({"status": "ok"})

    return jsonify({"status": "fail"}), 401

# ==============================
# ADMIN PANEL PAGE
# ==============================

@app.route("/admin")
def admin_panel():
    if not session.get("admin"):
        return render_template("admin.html")  
        # Shows login screen first
    return render_template("admin.html")

# ==============================
# ADMIN DATA APIs
# ==============================

@app.route("/admin/messages")
def admin_messages():
    if not session.get("admin"):
        return jsonify([]), 401

    try:
        messages = []
        
        if USE_MONGODB and contact_collection:
            msgs = contact_collection.find().sort("_id", -1)
            messages = [
                {
                    "name": m["name"],
                    "email": m["email"],
                    "phone": m.get("phone", ""),
                    "subject": m.get("subject", ""),
                    "message": m["message"]
                } for m in msgs
            ]
        else:
            conn = get_sqlite_db()
            cursor = conn.cursor()
            cursor.execute('SELECT name, email, phone, subject, message FROM contact_messages ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            messages = [
                {
                    "name": row["name"],
                    "email": row["email"],
                    "phone": row["phone"],
                    "subject": row["subject"],
                    "message": row["message"]
                } for row in rows
            ]
        
        return jsonify(messages)
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify([]), 500

@app.route("/admin/enquiries")
def admin_enquiries():
    if not session.get("admin"):
        return jsonify([]), 401

    try:
        enquiries = []
        
        if USE_MONGODB and enquiry_collection:
            enqs = enquiry_collection.find().sort("_id", -1)
            enquiries = [
                {
                    "product": e["product"],
                    "name": e["name"],
                    "country": e.get("country", ""),
                    "phone": e.get("phone", ""),
                    "email": e["email"]
                } for e in enqs
            ]
        else:
            conn = get_sqlite_db()
            cursor = conn.cursor()
            cursor.execute('SELECT product, name, country, phone, email FROM product_enquiries ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            enquiries = [
                {
                    "product": row["product"],
                    "name": row["name"],
                    "country": row["country"],
                    "phone": row["phone"],
                    "email": row["email"]
                } for row in rows
            ]
        
        return jsonify(enquiries)
    except Exception as e:
        print(f"Error fetching enquiries: {e}")
        return jsonify([]), 500

# ==============================
# ADMIN LOGOUT
# ==============================

@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_panel"))

# ==============================
# CUSTOM 404
# ==============================

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - Page Not Found</h1>", 404

# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    # app.run(debug=True)
     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))