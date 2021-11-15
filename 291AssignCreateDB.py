import pandas as pd
import sqlite3


conn = sqlite3.connect(r"smallDB.db")
cur = conn.cursor()

# create tables as specified in the assignment description
cur.execute('''CREATE TABLE IF NOT EXISTS Customers (customer_id TEXT, customer_postal_code	INTEGER, PRIMARY KEY(customer_id));''')
cur.execute('''CREATE TABLE IF NOT EXISTS Sellers (seller_id TEXT, seller_postal_code INTEGER, PRIMARY KEY(seller_id));''')
cur.execute('''CREATE TABLE IF NOT EXISTS Orders (order_id TEXT, customer_id TEXT, PRIMARY KEY(order_id),
	FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)); ''')
cur.execute('''CREATE TABLE Order_items (order_id TEXT,	order_item_id INTEGER, product_id TEXT,	seller_id TEXT,
	PRIMARY KEY(order_id,order_item_id,product_id,seller_id),
	FOREIGN KEY(seller_id) REFERENCES Sellers(seller_id)
	FOREIGN KEY(order_id) REFERENCES Orders(order_id)); ''')

customers = pd.read_csv(r"A3_CSV_files\olist_customers_dataset.csv")
customers = customers.loc[:, ['customer_id', 'customer_zip_code_prefix']].rename(
    columns={"customer_zip_code_prefix": "customer_postal_code"})
customers = customers.sample(n=10000)
customers.to_sql('Customers', conn, if_exists='append', index=False)

sellers = pd.read_csv(r"A3_CSV_files\olist_sellers_dataset.csv")
sellers = sellers.loc[:, ['seller_id', 'seller_zip_code_prefix']].rename(
    columns={"seller_zip_code_prefix": "seller_postal_code"})
sellers = sellers.sample(n=500)
sellers.to_sql('Sellers', conn, if_exists='append', index=False)

orders = pd.read_csv(r"A3_CSV_files\olist_orders_dataset.csv")
orders = orders.loc[:, ['order_id', 'customer_id']]
orders = orders.sample(n=10000)
orders.to_sql('Orders', conn, if_exists='append', index=False)

items = pd.read_csv(r"A3_CSV_files\olist_order_items_dataset.csv")
items = items.loc[:, ['order_id', 'order_item_id', 'product_id', 'seller_id']]
items = items.sample(n=2000)
items.to_sql('Order_items', conn, if_exists='append', index=False)

conn.close()
