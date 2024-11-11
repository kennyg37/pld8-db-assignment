from pydantic import BaseModel

class UserRequest(BaseModel):
    name: str
    email: str
    country_name: str
    gender: str
    age: int
    annual_salary: int
    credit_card: int
    net_worth: int
    car_purchase: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Alex Jones",
                "email": "alexjones@example.com",
                "country_name": "Bahrain",
                "gender": "male",
                "age": 30,
                "annual_salary": 55000,
                "credit_card": 1,
                "net_worth": 100000,
                "car_purchase": 1
            }
        }
