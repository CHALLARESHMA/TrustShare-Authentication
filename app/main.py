from fastapi import FastAPI
from app.schemas import UserRegister, UserLogin
from app.database import SessionLocal
from app.models import User
from app.security import hash_password, verify_password

app = FastAPI()




@app.get("/")
def home():
    return {"message": "TrustShare Backend Running Successfully"}

@app.post("/register")
def register(user: UserRegister):
    db = SessionLocal()

    hashed_password = hash_password(user.password)

    new_user = User(
    username=user.username,
    email=user.email,
    password=hashed_password
   )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "User Registered Successfully",
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }
@app.post("/login")
def login(user: UserLogin):
    db = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        db.close()
        return {"message": "User not found"}

    if not verify_password(user.password, db_user.password):
        db.close()
        return {"message": "Invalid password"}

    db.close()

    return {
        "message": "Login Successful",
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email
    }