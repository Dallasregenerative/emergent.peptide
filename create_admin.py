#!/usr/bin/env python3
"""
Create admin user for PeptideProtocols.ai
"""
import asyncio
import bcrypt
import uuid
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def create_admin_user():
    # MongoDB connection
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Check if admin already exists
    existing_admin = await db.users.find_one({"role": "admin"})
    if existing_admin:
        print("Admin user already exists!")
        print(f"Email: {existing_admin['email']}")
        return
    
    # Create admin user
    admin_id = str(uuid.uuid4())
    admin_email = "admin@peptideprotocols.ai"
    admin_password = "admin123"  # Change this!
    
    admin_doc = {
        "id": admin_id,
        "email": admin_email,
        "password": hash_password(admin_password),
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "is_approved": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await db.users.insert_one(admin_doc)
    
    print("✅ Admin user created successfully!")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
    print("🔑 Please change the password after first login!")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin_user())