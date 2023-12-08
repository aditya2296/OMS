from flask import Flask, render_template, request, flash, redirect, url_for
from validators import generate_secret_key, generate_customer_id, generate_item_id
import pandas as pd
from models import Customer, Item, db
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = { 'database1': 'sqlite:///item.db', }
app.secret_key = generate_secret_key()
valid_credentials = {'pmadmin': 'pass123'}
test_credentials = {'pmtest': 'pass123'}
item_detail = []
customer_detail = []
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')
    if login_id in valid_credentials and password == valid_credentials[login_id]:
        return redirect(url_for('dashboard'))
    elif login_id in test_credentials and password == test_credentials[login_id]:
        return redirect(url_for('order_booking'))
    else:
        flash('Invalid username or password.', 'error')
        return render_template('login.html', error='Invalid username or password.')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/item_details')
def item_details():
    items = Item.query.all()
    total_items_count = len(items)
    return render_template('item_details.html', item_details=items, total_items_count = total_items_count)

@app.route('/customer_details')
def customer_details():
    customers = Customer.query.all()
    total_customers_count = len(customers)
    return render_template('customer_details.html', customer_details=customers, total_customers_count=total_customers_count)

@app.route('/new_item')
def new_item():
    return render_template('new_item.html')

@app.route('/save_new_item', methods=['POST'])
def save_new_item():
    items = Item.query.all()
    newItemDate = request.form.get('newItemDate')
    newItemName = request.form.get('newItemName')
    newItemCompany = request.form.get('newItemCompany')
    newItemQuantity = request.form.get('newItemQuantity')
    newItemBrandName = request.form.get('brandName')
    newItemPrice = request.form.get('newItemPrice')
    newItemDiscount = request.form.get('newItemDiscount')
    serial_number_item = len(items) + 1

    new_item = Item(id=generate_item_id(), serial_number = serial_number_item, created_by = "pmadmin",modified_date = newItemDate , purchase_date = newItemDate, item_name = newItemName, item_company = newItemCompany, brand_name = newItemBrandName, quantity = newItemQuantity, mrp = newItemPrice, discount = newItemDiscount)
    db.session.add(new_item)
    db.session.commit()

    return 'OK', 200
@app.route('/insert_excel_page')
def insert_excel_page():
    return render_template('insert_excel_page.html')

@app.route('/insert_from_excel', methods=['POST'])
def insert_from_excel():
    try:
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if not file.filename.endswith('.xlsx'):
            return 'Invalid file format. Please upload an Excel file (.xlsx)', 400
        df = pd.read_excel(file)
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date']).dt.date
        item_serial_number = len(Item.query.all()) + 1
        for index, row in df.iterrows():
            new_item = Item(
                id = generate_item_id(),
                serial_number = item_serial_number + index,
                created_by = "pmadmin",
                modified_date = row['Purchase Date'],
                purchase_date = row['Purchase Date'],
                item_name = row['Item Name'],
                item_company = row['Item Group'],
                brand_name = row['Brand Name'],
                quantity = row['Quantity'],
                mrp = row['Mrp'],
                discount = row['Discount']
            )
            db.session.add(new_item)
        db.session.commit()
        file.close
        return redirect(url_for('item_details'))
    except Exception as e:
        return str(e), 500
    
@app.route('/new_customer')
def new_customer():
    return render_template('new_customer.html')

@app.route('/save_new_customer', methods=['POST'])
def save_new_customer():
    customers = Customer.query.all()
    newCustomerName = request.form.get('newCustomerName')
    newCustomerLocation = request.form.get('newCustomerLocation')
    newPhoneNumber = request.form.get('newPhoneNumber')
    newCustomerEmail = request.form.get('newCustomerEmail')
    customerBillingType = request.form.get('CustomerBillingType')
    customerDeliveryType = request.form.get('CustomerDeliveryType')
    customerRoute = request.form.get('Route')
    serial_number_customer = len(customers) + 1

    try:
        new_customer = Customer(id = generate_customer_id(), created_by = "pmadmin",serial_number = serial_number_customer, customer_name=newCustomerName, customer_location = newCustomerLocation, customer_phone_number = newPhoneNumber, customer_email=newCustomerEmail, customer_billing_type = customerBillingType, customer_delivery_type = customerDeliveryType, customer_route = customerRoute)
        db.session.add(new_customer)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return 'Mobile Number Already Exists', 400

    return 'OK', 200

@app.route('/insert_customer_page')
def insert_customer_page():
    return render_template('insert_customer_page.html')

@app.route('/insert_from_excel_customer', methods=['POST'])
def insert_from_excel_customer():
        try:
            if 'file' not in request.files:
                return 'No file part', 400
            file = request.files['file']
            if file.filename == '':
                return 'No selected file', 400
            if not file.filename.endswith('.xlsx'):
                return 'Invalid file format. Please upload an Excel file (.xlsx)', 400
            df = pd.read_excel(file)
            customer_serial_number = len(Customer.query.all()) + 1
            for index, row in df.iterrows():
                new_customer = Customer (
                    id = generate_customer_id(),
                    created_by = "pmadmin",
                    serial_number = customer_serial_number + index,
                    customer_name=row['Customer_Name'],
                    customer_location=row['Location'],
                    customer_phone_number=row['Mobile_Number'],
                    customer_email=row['Email'],
                    customer_billing_type=row['Billing_Type'],
                    customer_delivery_type=row['Delivery_Type'],
                    customer_route=row['Route']
                )
                db.session.add(new_customer)
            db.session.commit()
            file.close
            return redirect(url_for('customer_details'))
        except Exception as e:
            return str(e), 500

@app.route('/order_booking')
def order_booking():
    return render_template('order_booking.html')

@app.route('/new_order')
def new_order():
    return render_template('new_order.html')

@app.route('/edit_customer/<string:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    original_id = customer_id
    if request.method == 'POST':
        customer.customer_name = request.form.get('newCustomerName')
        customer.customer_location = request.form.get('newCustomerLocation')
        customer.customer_phone_number = request.form.get('newPhoneNumber')
        customer.customer_email = request.form.get('newCustomerEmail')
        customer.customer_billing_type = request.form.get('CustomerBillingType')
        customer.customer_delivery_type = request.form.get('CustomerDeliveryType')
        customer.customer_route = request.form.get('Route')
        customer.id = original_id
        db.session.commit()
        return redirect(url_for('customer_details'))
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<string:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    serial_customer_id = int(customer_id[7:])
    db.session.delete(customer)
    customers_to_update = Customer.query.filter(Customer.serial_number > serial_customer_id).all()
    for customer in customers_to_update:
        customer.serial_number -= 1
    db.session.commit()
    return redirect(url_for('customer_details'))

@app.route('/edit_item/<string:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    original_id = item_id
    if request.method == 'POST':
        item.purchase_date = request.form.get('newItemDate')
        item.modified_date = request.form.get('editItemDate')
        item.item_name = request.form.get('newItemName')
        item.item_company = request.form.get('newItemCompany')
        item.brand_name = request.form.get('brandName')
        item.quantity = request.form.get('newItemQuantity')
        item.mrp = request.form.get('newItemPrice')
        item.discount = request.form.get('newItemDiscount')
        item.id = original_id
        db.session.commit()
        return redirect(url_for('item_details'))
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<string:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    serial_item_id = int(item_id[8:])
    db.session.delete(item)
    item_to_update = Item.query.filter(Item.serial_number > serial_item_id).all()
    for item in item_to_update:
        item.serial_number -= 1
    db.session.commit()
    return redirect(url_for('item_details'))
if __name__ == '__main__':
    app.run(debug=True)
