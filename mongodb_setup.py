"""
MongoDB Connection Diagnostic Script
Run this to diagnose MongoDB connectivity issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://shastikaAdmin:3mlwFIzs28o9cpT2@shastika.uruv1ox.mongodb.net/?appName=shastika"
)

print("=" * 60)
print("MONGODB CONNECTION DIAGNOSTIC")
print("=" * 60)

print(f"\n1. Connection String:")
print(f"   {MONGO_URI[:50]}...")

print(f"\n2. Testing DNS Resolution...")
import socket
try:
    # Extract hostname from URI
    hostname = MONGO_URI.split("@")[1].split("/")[0]
    print(f"   Hostname: {hostname}")
    ip = socket.gethostbyname(hostname)
    print(f"   ✓ Resolved to IP: {ip}")
except socket.gaierror as e:
    print(f"   ✗ DNS Resolution Failed: {e}")
    print(f"   → Check if MongoDB Atlas cluster exists")
    print(f"   → Check MongoDB Atlas IP Whitelist settings")
except Exception as e:
    print(f"   ✗ Error: {e}")

print(f"\n3. Testing MongoDB Connection...")
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print(f"   ✓ MongoDB Connection Successful!")
    
    # List databases
    databases = client.list_database_names()
    print(f"   Databases: {databases}")
    
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"   ✗ Connection Failed: {e}")
    print(f"   → Add your IP to MongoDB Atlas Network Access")
    
    # Get current public IP
    try:
        import requests
        response = requests.get('https://api.ipify.org?format=json', timeout=3)
        public_ip = response.json()['ip']
        print(f"   → Your Public IP: {public_ip}")
        print(f"   → MongoDB Atlas > Network Access > Add your IP")
    except:
        import socket
        print(f"   → Open MongoDB Atlas and add your current IP to whitelist")
        
except Exception as e:
    print(f"   ✗ Unexpected Error: {e}")

print("\n" + "=" * 60)
print("SOLUTIONS:")
print("=" * 60)
print("""
1. Go to MongoDB Atlas: https://www.mongodb.com/cloud/atlas
2. Login with your account
3. Select your project/cluster
4. Navigate to: Network Access (or Security > Network Access)
5. Click "Add IP Address"
6. Options:
   a) Add current IP only (more secure)
   b) Allow from anywhere: 0.0.0.0/0 (for testing only)
7. Click "Confirm"
8. Wait 1-2 minutes for changes to apply
9. Run this script again to test

Alternative: Use local MongoDB
- Install MongoDB Community Edition locally
- Update MONGO_URI to: mongodb://localhost:27017/shastikaDB
""")
