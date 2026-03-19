from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==============================
# APP CONFIG
# ==============================

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "SHASTIKA_ADMIN_PANEL_KEY_2025")

# ==============================
# MONGODB CONNECTION
# ==============================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://shastikaAdmin:3mlwFIzs28o9cpT2@shastika.uruv1ox.mongodb.net/?appName=shastika"
)

client = None
db = None
contact_collection = None
enquiry_collection = None

def connect_to_mongodb():
    """Initialize MongoDB connection"""
    global client, db, contact_collection, enquiry_collection
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.admin.command('ping')
        db = client["shastikaDB"]
        
        contact_collection = db["contact_messages"]
        enquiry_collection = db["product_enquiries"]
        
        print("✓ MongoDB connected successfully")
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error connecting to MongoDB: {e}")
        return False

# Connect to MongoDB on startup
connect_to_mongodb()
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


# ==============================
# DYNAMIC PRODUCT PAGES
# ==============================

@app.route("/product/<product_name>")
def product_page(product_name):
    try:
        return render_template(f"products/{product_name}.html")
    except:
        abort(404)

# ==============================
# CONTACT FORM API
# ==============================

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    if not contact_collection:
        return jsonify({"status": "error", "message": "Database unavailable"}), 503
    
    try:
        data = request.json
        contact_collection.insert_one({
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "subject": data.get("subject"),
            "message": data.get("message")
        })
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error inserting contact: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ==============================
# PRODUCT ENQUIRY API
# ==============================

@app.route("/submit_enquiry", methods=["POST"])
def submit_enquiry():
    if not enquiry_collection:
        return jsonify({"status": "error", "message": "Database unavailable"}), 503
    
    try:
        data = request.json
        enquiry_collection.insert_one({
            "product": data.get("product"),
            "name": data.get("name"),
            "country": data.get("country"),
            "phone": data.get("phone"),
            "email": data.get("email")
        })
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

    msgs = contact_collection.find().sort("_id", -1)

    return jsonify([
        {
            "name": m["name"],
            "email": m["email"],
            "phone": m["phone"],
            "subject": m["subject"],
            "message": m["message"]
        } for m in msgs
    ])

@app.route("/admin/enquiries")
def admin_enquiries():
    if not session.get("admin"):
        return jsonify([]), 401

    enqs = enquiry_collection.find().sort("_id", -1)

    return jsonify([
        {
            "product": e["product"],
            "name": e["name"],
            "country": e["country"],
            "phone": e["phone"],
            "email": e["email"]
        } for e in enqs
    ])

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
    app.run(debug=True)