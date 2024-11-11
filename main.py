import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session  
from sqlalchemy.exc import IntegrityError
from src.models.schema import UserRequest
from src.models.models import Countries, User, User_data
from src.config import get_db
from src.populate import populate_databases, populate_mongodb
import uvicorn

load_dotenv()

app = FastAPI()

port = int(os.getenv("PORT"))

@app.get("/", include_in_schema=False)
def read_root(session: Session = Depends(get_db)):
    return RedirectResponse(url="/docs")

@app.post("/populate/postgres")
def populate_db(session: Session = Depends(get_db)):
    populate_databases(session)
    return {"message": "Database populated"}

@app.post("/users/")
async def create_user(user_data: UserRequest, request: Request, session: Session = Depends(get_db)):
    user_data = await request.json()
    
    existing_user = session.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user = User(
        name=user_data["name"],
        email=user_data["email"]
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    country = session.query(Countries).filter(Countries.country_name == user_data["country_name"]).first()
    if not country:
        try:
            new_country = Countries(country_name=user_data["country_name"])
            session.add(new_country)
            session.commit()
            session.refresh(new_country)
            country = new_country
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=500, detail="Error adding new country")

    new_user_data = User_data(
        user_id=new_user.id,
        country_id=country.id,
        gender=user_data["gender"],
        age=user_data["age"],
        annual_salary=user_data["annual_salary"],
        credit_card=user_data["credit_card"],
        net_worth=user_data["net_worth"],
        car_purchase=user_data["car_purchase"]
    )

    session.add(new_user_data)
    session.commit()
    session.refresh(new_user_data)

    return {"id": str(new_user.id)}
@app.get("/users/")
def get_last_user(session: Session = Depends(get_db)):
    user = session.query(User).order_by(User.id.desc()).first()
    user_data = session.query(User_data).filter(User_data.user_id == user.id).first() if user else None

    if not user or not user_data:
        return {}

    country = session.query(Countries).filter(Countries.id == user_data.country_id).first() if user_data else None

    user_data_dict = user_data.__dict__ if user_data else {}
    user_data_dict.update(user.__dict__ if user else {})

    if country:
        user_data_dict["country_name"] = country.country_name
    last_user_dict = {k: v for k, v in user_data_dict.items() if not k.startswith("_")}
    
    return last_user_dict

@app.get("/users/{user_id}")
def get_user(user_id: uuid.UUID, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = session.query(User_data).filter(User_data.user_id == user.id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User data not found")

    user_data_dict = user_data.__dict__
    user_data_dict.update(user.__dict__)
    
    return {k: v for k, v in user_data_dict.items() if not k.startswith("_")}

@app.put("/users/{user_id}")
async def update_user(user_data:UserRequest, user_id: uuid.UUID, request: Request, session: Session = Depends(get_db)):
    user_data = await request.json()
    
    existing_user = session.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user_data["name"]
    existing_user.email = user_data["email"]
    session.commit()

    existing_user_data = session.query(User_data).filter(User_data.user_id == user_id).first()
    if not existing_user_data:
        raise HTTPException(status_code=404, detail="User data not found")

    existing_user_data.gender = user_data["gender"]
    existing_user_data.age = user_data["age"]
    existing_user_data.annual_salary = user_data["annual_salary"]
    existing_user_data.credit_card = user_data["credit_card"]
    existing_user_data.net_worth = user_data["net_worth"]
    existing_user_data.car_purchase = user_data["car_purchase"]
    session.commit()

    return {"status": "User and user data updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: uuid.UUID, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = session.query(User_data).filter(User_data.user_id == user_id).first()
    if user_data:
        session.delete(user_data)
    session.delete(user)
    session.commit()

    return {"status": "User and user data deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
