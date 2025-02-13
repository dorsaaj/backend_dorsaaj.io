from fastapi import FastAPI, Form
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Example: Access the secret key or database URL from the environment
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL instead of "*" for security reasons
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
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
    created_at = Column(TIMESTAMP)

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
    new_message = ContactMessage(
        name=form.name, 
        email=form.email, 
        message=form.message
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    db.close()
    return {"message": "Thank you for contacting us!"}

