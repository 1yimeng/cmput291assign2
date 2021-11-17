import pandas as pd
import sqlite3


# A3Small.db      A3Medium.db     A3Large.db
conn = sqlite3.connect(r"A3Test.db")
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
# remove duplicates for primary key
customers = customers.drop_duplicates(subset='customer_id')
customers = customers.sample(n=10000)  # 10000    20000   33000
customers.to_sql('Customers', conn, if_exists='append', index=False)

sellers = pd.read_csv(r"A3_CSV_files\olist_sellers_dataset.csv")
sellers = sellers.loc[:, ['seller_id', 'seller_zip_code_prefix']].rename(
    columns={"seller_zip_code_prefix": "seller_postal_code"})
# remove duplicates for primary key
sellers = sellers.drop_duplicates(subset='seller_id')
sellers = sellers.sample(n=500)  # 500     750   1000
sellers.to_sql('Sellers', conn, if_exists='append', index=False)

orders = pd.read_csv(r"A3_CSV_files\olist_orders_dataset.csv")
orders = orders.loc[:, ['order_id', 'customer_id']]
# remove duplicates for primary key
orders = orders.drop_duplicates(subset='order_id')
cids = customers['customer_id'].tolist()
drop = []
for i in range(len(orders)):
    if orders.iloc[i, 1] not in cids:
        drop.append(i)
orders.drop(drop, inplace=True)
orders = orders.sample(n=10000)  # 10000    20000     33000
orders.to_sql('Orders', conn, if_exists='append', index=False)

items = pd.read_csv(r"A3_CSV_files\olist_order_items_dataset.csv")
items = items.loc[:, ['order_id', 'order_item_id', 'product_id', 'seller_id']]
# remove duplicates for primary key
items = items.drop_duplicates()
sids = sellers['seller_id'].tolist()
oids = orders['order_id'].tolist()
drop = []
for i in range(len(items)):
    if items.iloc[i, 3] not in sids:
        drop.append(i)
    elif items.iloc[i, 0] not in oids:
        drop.append(i)
items.drop(drop, inplace=True)
print(items.size)
num = max(items.size, 2000)
items = items.sample(n=num)  # 2000     4000     10000
items.to_sql('Order_items', conn, if_exists='append', index=False)

conn.close()
