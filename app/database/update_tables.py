from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.interviews_table import Interviews
from app.models.customer_table import Customers
from app.models.hypotheses_table import Hypotheses


def update_hypotheses(db: Session, hypothesis_analysis_func):
    # pass in analysis function -> can change to pass in specifically scores / output
    
    # only analyze based on value of evaluated
    hypos = db.query(Hypotheses).filter(Hypotheses.evaluated == False).all()
    
    # assumes analysis func returns a dictionary (but again can be updated)
    for h in hypos:
        result = hypothesis_analysis_func(h.embedding) # pass embedding for analysis
        
        # update output
        h.hypotheses_output = result.get("reasoning")
        
        # update score
        h.hypotheses_output_score = int(result.get("score", 0))
        
        # update suggested customers
        h.suggested_customer_profiles = result.get("profiles")

        h.evalulated = True
        
        # for debugging
        print(f"Scored: {h.hypotheses_output_score}/10 | Profiles Suggested: {len(h.suggested_customer_profiles)}")
        
    db.commit()
    
# similar assumptions:

def update_customers(db: Session, customer_analysis_func):
    customers = db.query(Customers).filter(Customers.customer_checked == False).all()
    
    # if all customers have already been checked
    if not customers:
        print("No customers to update.")
        return
    
    for customer in customers:
        # give context (update depending on what is required)
        context = f"Name: {customer.customer_name}, Role: {customer.customer_occupation}, Industry: {customer.customer_industry}"
        
        ai_result = customer_analysis_func(context)
        
        customer.customers_output = ai_result.get("profile")
        customer.customers_output_score = ai_result.get("score")
        
        customer.customer_checked = True
        print(f"Updated Customer: {customer.customer_name}")

    db.commit()

def update_interviews(db: Session, interview_analysis_func):
    interviews = db.query(Interviews).filter(Interviews.checked == False).all()
    