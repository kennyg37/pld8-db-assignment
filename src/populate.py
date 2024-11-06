import pandas as pd
from sqlalchemy.orm import Session
from src.models.models import User, Countries, User_data

def populate_postgres(session: Session, dataframe: pd.DataFrame):
    unique_countries = dataframe['country'].unique()
    for country in unique_countries:
        country_entry = Countries(country_name=country)
        session.add(country_entry)
    session.commit()

    country_map = {c.country_name: c.id for c in session.query(Countries).all()}
    
    for index, row in dataframe.iterrows():
        user = User(name=row['customer name'], email=row['customer e-mail'])
        session.add(user)
        session.commit() 
        user_data = User_data(
            user_id=user.id,
            country_id=country_map[row['country']],
            gender=row['gender'],
            age=row['age'],
            annual_salary=row['annual Salary'],
            credit_card=row['credit card debt'],
            net_worth=row['net worth'],
            car_purchase=row['car purchase amount']
        )
        session.add(user_data)

    session.commit()

def populate_databases(session: Session):
    dataframe = pd.read_csv("data/car_purchasing.csv", encoding="ISO-8859-1")
    populate_postgres(session, dataframe)
