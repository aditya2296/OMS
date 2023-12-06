import secrets
from models import Customer, Item

def generate_secret_key():
    return secrets.token_hex(16)

def generate_customer_id():
    last_customer = Customer.query.order_by(Customer.id.desc()).first()

    if last_customer:
        last_serial = int(last_customer.id.split('T')[-1])
        new_serial = last_serial + 1
    else:
        new_serial = 1
        
    return f"CUST{new_serial:04d}"

def generate_item_id():
    last_item = Item.query.order_by(Item.id.desc()).first()

    if last_item:
        last_serial = int(last_item.id.split('M')[-1])
        new_serial = last_serial + 1
    else:
        new_serial = 1
    return f"ITEM{new_serial:05d}"