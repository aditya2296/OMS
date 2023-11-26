import secrets, sqlite3

def generate_secret_key():
    return secrets.token_hex(16)

def create_customers_table():
    conn = sqlite3.connect('customer_details_table.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS customer_details_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customername TEXT NOT NULL,
            customerlocation TEXT NOT NULL,
            customerphonenumber INTEGER NOT NULL,
            customeremail TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
