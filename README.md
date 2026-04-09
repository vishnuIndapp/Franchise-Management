# Franchise-Management
# 🚀 FastAPI Franchise Management System

A scalable backend system built with **FastAPI**, supporting **Super Admin & Franchise authentication**, JWT security, OTP verification, Redis caching, and PostgreSQL database.

---

## 📌 Features

- 🔐 JWT Authentication (Access + Refresh Token)
- 👤 Super Admin & Franchise Login (Single Endpoint)
- 📧 Email OTP Verification (SMTP)
- ⚡ Redis Caching (OTP + Sessions)
- 🏢 Franchise Management (CRUD APIs)
- 👤 Profile Management APIs
- 🗄️ PostgreSQL Database with SQLAlchemy ORM
- 🔄 Refresh Token Mechanism
- 🌐 REST API with Swagger Docs
- 🚀 Ready for AWS Deployment

---





## ⚙️ Installation

### 1️⃣ Clone Repository


---

### 2️⃣ Create Virtual Environment
- python -m venv env


---

### 3️⃣ Install Dependencies
- pip install -r requirements.txt

## 🗄️ Database Setup (PostgreSQL)
- CREATE DATABASE Franchise;


---

## 🔐 Environment Variables (.env)

Database

DATABASE_URL=postgresql://postgres:password@localhost:5432/franchise_db

JWT

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SMTP Email

EMAIL_FROM=your_email@gmail.com

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com

SMTP_PASSWORD=your_app_password

Redis

REDIS_URL=redis://localhost:6379

OTP

OTP_EXPIRATION_SECONDS=300



---

## ▶️ Run Application

uvicorn app.main:app --host 0.0.0.0 --port 8000


## For Creating admin user 



        from app.core.database import SessionLocal
        from app.models.user import User, Role
        from passlib.context import CryptContext
        from app.core.security import hash_password
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


        @app.on_event("startup")
        def create_admin():
            db = SessionLocal()
            try:
                admin_email = "superadmin@gmail.com"
                admin_password = "Super@123"

                admin = db.query(User).filter(User.email == admin_email).first()

                if not admin:
                    new_admin = User(
                        email=admin_email,
                        password=hash_password(admin_password),
                        role=Role.SUPER_ADMIN
                    )
                    db.add(new_admin)
                    db.commit()
                    # logger.info("✅ Super Admin created")
                else:
                    print("ℹ️ Super Admin already exists")
                    # logger.info("ℹ️ Super Admin already exists")

            except Exception as e:
                print(f"❌ Error creating admin: {str(e)}")
                # logger.error(f"❌ Error creating admin: {str(e)}")
            finally:
                db.close()

RUN THE CODE IN main.py while app startup




