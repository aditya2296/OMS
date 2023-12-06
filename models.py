from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    customer_name = db.Column(db.String(255))
    customer_location = db.Column(db.String(255))
    customer_phone_number = db.Column(db.Integer)
    customer_email = db.Column(db.String(255))
    customer_billing_type = db.Column(db.String(255))
    customer_delivery_type = db.Column(db.String(255))
    customer_route = db.Column(db.String(255))

    def __repr__(self):
        return f"<Customer {self.id}: {self.name}>"

class Item(db.Model):
    __bind_key__ = 'database1'
    id = db.Column(db.String(20), primary_key=True)
    purchase_date = db.Column(db.String(255))
    modified_date = db.Column(db.String(255))
    item_name = db.Column(db.String(255))
    item_company = db.Column(db.String(255))
    brand_name = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    mrp = db.Column(db.Integer)
    discount = db.Column(db.Integer)

def init_db(app):
    # Initialize the database with the Flask app
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

# Other model definitions and configurations...
