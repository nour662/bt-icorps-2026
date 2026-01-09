import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv #dotenv to read from env
from sqlalchemy.orm import Session
from app.models.customer_table import Customers



def save_(db: Session, 
          team_id: str, 
          name: str, 
          industry: str, 
          occupation: str, 
          experience: str,
          checked: bool = False):

    # creating database object
    new_customer = Customers(
        team_id = team_id,
        customer_name = name,
        customer_industry = industry,
        customer_occupation = occupation,
        customer_experience = experience,
        customer_checked = checked,  # initialized to be false upon creation
        customers_output = "",       # intialize to be empty
        customers_output_score = 0   # set to be 0 for now
    )    
    try:
        db.add(new_customer)
        db.commit()
        print(f"Successfully created customer: {new_customer.customer_name}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
