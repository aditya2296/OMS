from flask import Flask, render_template, request, flash, redirect, url_for
from validators import generate_secret_key, create_customers_table
import pandas as pd, sqlite3

app = Flask(__name__, template_folder="templates")
app.secret_key = generate_secret_key()
valid_credentials = {'pmadmin': 'pass123'}
test_credentials = {'pmtest': 'pass123'}
item_detail = []
customer_detail = []
create_customers_table()

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
    return render_template('item_details.html', item_details=item_detail)

@app.route('/customer_details')
def customer_details():
    conn = sqlite3.connect('customer_details_table.db')
    c = conn.cursor()
    c.execute('SELECT * FROM customer_details_table')
    customer_details_table = c.fetchall()
    conn.close()
    return render_template('customer_details.html', customer_details=customer_details_table)

@app.route('/new_item')
def new_item():
    return render_template('new_item.html')

@app.route('/save_new_item', methods=['POST'])
def save_new_item():
    newItemDate = request.form.get('newItemDate')
    newItemName = request.form.get('newItemName')
    newItemCompany = request.form.get('newItemCompany')
    newItemQuantity = request.form.get('newItemQuantity')
    newItemPrice = request.form.get('newItemPrice')
    newItemDiscount = request.form.get('newItemDiscount')

    new_item = {
        'Date of Purchase': newItemDate,
        'Item Name': newItemName,
        'Company Name': newItemCompany,
        'Quantity': int(newItemQuantity),
        'Price': int(newItemPrice),
        'Discount': int(newItemDiscount)
    }
    item_detail.append(new_item)

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
        new_items = df.iloc[:, :].to_dict(orient='records')
        item_detail.extend(new_items)
        file.close
        return render_template('item_details.html', item_details=item_detail)

    except Exception as e:
        return str(e), 500
    
@app.route('/new_customer')
def new_customer():
    return render_template('new_customer.html')

@app.route('/save_new_customer', methods=['POST'])
def save_new_customer():
    newCustomerName = request.form.get('newCustomerName')
    newCustomerLocation = request.form.get('newCustomerLocation')
    newPhoneNumber = request.form.get('newPhoneNumber')
    newCustomerEmail = request.form.get('newCustomerEmail')
    
    conn = sqlite3.connect('customer_details_table.db')
    c = conn.cursor()
    c.execute('INSERT INTO customer_details_table (customername, customerlocation, customerphonenumber, customeremail) VALUES (?, ?, ?, ?)', (newCustomerName, newCustomerLocation, newPhoneNumber, newCustomerEmail))
    conn.commit()
    conn.close()

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
        new_customers = df.iloc[:, :].to_dict(orient='records')
        customer_detail.extend(new_customers)
        file.close

        return render_template('customer_details.html', customer_details = customer_detail)

    except Exception as e:
        return str(e), 500
    
@app.route('/order_booking')
def order_booking():
    return render_template('order_booking.html')

@app.route('/new_order')
def new_order():
    return render_template('new_order.html')


if __name__ == '__main__':
    app.run(debug=True)
