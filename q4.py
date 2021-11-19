import sqlite3
import matplotlib.pyplot as plt
import random
import time

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def multi_bar_chart(values1, values2, values3, labels, title):
    # if lists empty print warning
    if len(values1) < 1 or len(values2) < 1 or len(values3) < 1:
        print('Warning: empty input so generated plot will be empty')

    width = 0.35
    fig, ax = plt.subplots()
    bottoms = [a+b for a,b in zip(values1, values2)]
    ax.bar(labels, values1, width, label="Uninformed")
    ax.bar(labels, values2, width, label="Self-Optimized", bottom=values1)
    ax.bar(labels, values3, width, label="User-Optimized", bottom=bottoms)

    # label x and y axis
    plt.xticks(range(len(labels)), labels)
    plt.legend()

    # give plot a title
    plt.title(title)

    # save plot to file
    # we'll use passed title to give file name
    path = './Q4A3chart.png'
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))

    # close figure so it doesn't display
    plt.close()
    return

def get_all_order_id():
    global connection, cursor
    cursor.execute(f'SELECT DISTINCT order_id FROM Orders')
    rows = cursor.fetchall()
    all_order = []
    for row in rows:
        all_order.append(row[0])
    return all_order

def run_50_time():
    global connection, cursor
    all_random_id = get_all_order_id()
    random_id = []
    for i in range(50):
        random_id.append(random.choice(all_random_id))
    start = time.time() 
    for i in range(50):
        cursor.execute('SELECT COUNT(DISTINCT S.seller_postal_code) FROM Order_items O, Sellers S WHERE S.seller_id = O.seller_id AND O.order_id = ?', (random_id[i],))
    end = time.time()
  
    connection.commit()
    final = (end - start) * 1000
    return end-start

def uninformed():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = FALSE')
    cursor.execute('''CREATE TABLE IF NOT EXISTS "Order_itemsNEW" (
        order_id TEXT,
        order_item_id INTEGER,
        product_id TEXT,
        seller_id TEXT)''')
    cursor.execute('INSERT INTO Order_itemsNEW SELECT order_id, order_item_id, product_id, seller_id FROM Order_items')
    cursor.execute('ALTER TABLE Order_items RENAME TO Order_itemsOriginal')
    cursor.execute('ALTER TABLE Order_itemsNEW RENAME TO Order_items')

    cursor.execute('''CREATE TABLE IF NOT EXISTS "SellersNEW" (
	    seller_id TEXT,
	    seller_postal_code INTEGER)''')
    cursor.execute('INSERT INTO SellersNEW SELECT seller_id, seller_postal_code FROM Sellers')
    cursor.execute('ALTER TABLE Sellers RENAME TO SellersOriginal')
    cursor.execute('ALTER TABLE SellersNEW RENAME TO Sellers')

def uninformed_revert():
    cursor.execute('DROP TABLE Order_items')
    cursor.execute('ALTER TABLE Order_itemsOriginal RENAME TO Order_items')

    cursor.execute('DROP TABLE Sellers')
    cursor.execute('ALTER TABLE SellersOriginal RENAME TO Sellers')

def uninformed_revert():
    cursor.execute('DROP TABLE Order_items')
    cursor.execute('ALTER TABLE Order_itemsOriginal RENAME TO Order_items')

    cursor.execute('DROP TABLE Sellers')
    cursor.execute('ALTER TABLE SellersOriginal RENAME TO Sellers')
   
def db_uninformed(path):
    global connection, cursor
    connect(path)
    uninformed()
    time_taken = run_50_time()
    uninformed_revert()
    connection.commit()
    connection.close()
    return time_taken

def db_self_optimized(path):
    global connection, cursor
    connect(path)
    cursor.execute('PRAGMA automatic_index = TRUE')
    time_taken = run_50_time()
    connection.commit()
    connection.close()
    return time_taken

def db_user_optimized(path):
    global connection, cursor
    connect(path)
    # user_optimized()
    uninformed()
    cursor.execute('CREATE INDEX Sellerid1 ON Sellers (seller_id)')
    cursor.execute('CREATE INDEX Sellerid ON Order_items (seller_id)')
    cursor.execute('CREATE INDEX orderid ON Order_items (order_id)')
    time_taken = run_50_time()
    connection.commit()
    connection.close()
    return time_taken

def main():
    global connection, cursor
    paths = ["./A3Small.db", "./A3Medium.db", "./A3Large.db"]
    uninformed_time = []
    self_optimized_time = []
    user_optimized_time = []

    for path in paths:
        uninformed_ms = db_uninformed(path) * 1000
        uninformed_time.append(uninformed_ms)
        self_optimized_ms = db_self_optimized(path) * 1000
        self_optimized_time.append(self_optimized_ms)
        user_optimized_ms = db_user_optimized(path) * 1000
        user_optimized_time.append(user_optimized_ms)

    labels = ['SmallDB', 'MediumDB', 'LargeDB']
    print(uninformed_time)
    print(self_optimized_time)
    print(user_optimized_time)
    multi_bar_chart(uninformed_time, self_optimized_time, user_optimized_time, labels, 'Q4 (Runtime in ms)')
    return

if __name__ == "__main__":
    main()

