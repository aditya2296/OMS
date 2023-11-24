from flask import Flask, render_template, request, flash, redirect, url_for
from validators import generate_secret_key
import pandas as pd

app = Flask(__name__, template_folder="templates")
app.secret_key = generate_secret_key()

# Hardcoded user credentials (replace this with a proper authentication mechanism)
valid_credentials = {'pmadmin': 'pass123'}
item_detail = []
customer_detail = []

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')
    if login_id in valid_credentials and password == valid_credentials[login_id]:
        # Successful login, redirect to the home page (you can replace 'home' with your actual home route)
        return redirect(url_for('dashboard'))
    else:
        # Incorrect credentials, show an error message (you can improve this part)
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
    return render_template('customer_details.html', customer_details=customer_detail)

@app.route('/new_item')
def new_item():
    return render_template('new_item.html')

@app.route('/save_new_item', methods=['POST'])
def save_new_item():
    # Retrieve data from the request
    newItemDate = request.form.get('newItemDate')
    newItemName = request.form.get('newItemName')
    newItemCompany = request.form.get('newItemCompany')
    newItemQuantity = request.form.get('newItemQuantity')
    newItemPrice = request.form.get('newItemPrice')

    # Add the new item to the item_details dictionary
    new_item = {
        'Date of Purchase': newItemDate,
        'Item Name': newItemName,
        'Company Name': newItemCompany,
        'Quantity': int(newItemQuantity),
        'Price': float(newItemPrice)
    }
    item_detail.append(new_item)

    return 'OK', 200
@app.route('/insert_excel_page')
def insert_excel_page():
    return render_template('insert_excel_page.html')

@app.route('/insert_from_excel', methods=['POST'])
def insert_from_excel():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        # Check if the file is uploaded
        if file.filename == '':
            return 'No selected file', 400

        # Check if the file is an Excel file
        if not file.filename.endswith('.xlsx'):
            return 'Invalid file format. Please upload an Excel file (.xlsx)', 400

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file)

        # Extract the rows (excluding the header) as a list of dictionaries
        new_items = df.iloc[:, :].to_dict(orient='records')

        # Add the new items to the item_details list
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
    # Retrieve data from the request
    newCustomerName = request.form.get('newCustomerName')
    newPhoneNumber = request.form.get('newPhoneNumber')

    # Add the new item to the item_details dictionary
    new_customer = {
        'Customer Name': newCustomerName,
        'Mobile Number': int(newPhoneNumber)
    }
    customer_detail.append(new_customer)

    return 'OK', 200

@app.route('/insert_customer_page')
def insert_customer_page():
    return render_template('insert_customer_page.html')

@app.route('/insert_from_excel_customer', methods=['POST'])
def insert_from_excel_customer():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        # Check if the file is uploaded
        if file.filename == '':
            return 'No selected file', 400

        # Check if the file is an Excel file
        if not file.filename.endswith('.xlsx'):
            return 'Invalid file format. Please upload an Excel file (.xlsx)', 400

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file)

        # Extract the rows (excluding the header) as a list of dictionaries
        new_customers = df.iloc[:, :].to_dict(orient='records')

        # Add the new customers to the customer_details list
        customer_detail.extend(new_customers)
        file.close

        return render_template('customer_details.html', customer_details = customer_detail)

    except Exception as e:
        return str(e), 500
if __name__ == '__main__':
    app.run(debug=True)
