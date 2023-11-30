import secrets
from models import Customer

def generate_secret_key():
    return secrets.token_hex(16)

def generate_customer_id():
    # Generate a unique customer ID with the format "cust_0001"
    last_customer = Customer.query.order_by(Customer.id.desc()).first()

    if last_customer:
        last_serial = int(last_customer.id.split('_')[-1])
        new_serial = last_serial + 1
    else:
        new_serial = 1
        
    return f"cust_{new_serial:04d}"
