from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the database URL from the environment
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise Exception("SQLALCHEMY_DATABASE_URL environment variable not set.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow GitHub Pages frontend
    allow_credentials=True,
    allow_methods=["POST"],  # Only allow POST requests
    allow_headers=["*"], 
)

# SQLAlchemy setup
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Contact Form Database Model
class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for form validation
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/contact")
async def send_contact(form: ContactForm):
    db = SessionLocal()
    try:
        new_message = ContactMessage(
            name=form.name, 
            email=form.email, 
            message=form.message
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return {"message": "Thank you for contacting us!"}
    except Exception as e:
        db.rollback()
        # Log the error (you might want to use logging instead of print in production)
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="There was an issue submitting your form.")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)


