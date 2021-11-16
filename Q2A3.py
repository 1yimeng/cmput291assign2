import sqlite3
import matplotlib.pyplot as plt
import random
import time

connection = None
cursor = None


def multi_bar_chart(values1, values2, values3, labels, title):
    # if lists empty print warning
    if len(values1) < 1 or len(values2) < 1 or len(values3) < 1:
        print('Warning: empty input so generated plot will be empty')

    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(labels, values1, width, label="Uninformed")
    ax.bar(labels, values2, width, label="Self-Optimized",  bottom=values1)
    ax.bar(labels, values3, width, label="User-Optimized",  bottom=values2)

    # label x and y axis
    plt.xticks(range(len(labels)), labels)
    plt.legend()

    # give plot a title
    plt.title(title)

    # save plot to file
    # we'll use passed title to give file name
    path = './Q2A3chart.png'
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))

    # close figure so it doesn't display
    plt.close()
    return


def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def query():
    global connection, cursor

    # get add postal codes and randomly select one
    cursor.execute("""SELECT DISTINCT(customer_postal_code) from Customers""")
    rows = cursor.fetchall()
    index = random.randint(0, len(rows)-1)
    postalCode = rows[index][0]

    cursor.execute("""CREATE VIEW IF NOT EXISTS OrderSize AS SELECT O.order_id as oid, COUNT(order_item_id) as size
	            FROM Orders as O, Order_items as I WHERE O.order_id = I.order_id GROUP BY O.order_id;""")
    cursor.execute("""SELECT AVG(size) FROM Customers as C, Orders as O, OrderSize WHERE customer_postal_code = :P
    AND C.customer_id = O.customer_id AND O.order_id = oid;""", {"P": postalCode})

    # get result
    result = cursor.fetchone()[0]
    connection.commit()
    return result


def scenario1():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = FALSE;')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS NewCustomers (customer_id TEXT, customer_postal_code INTEGER);''')
    cursor.execute(
        '''INSERT INTO NewCustomers SELECT customer_id, customer_postal_code FROM Customers;''')
    cursor.execute(
        '''ALTER TABLE Customers RENAME TO CustomersOriginal;''')
    cursor.execute(
        '''ALTER TABLE NewCustomers RENAME TO Customers;''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS NewOrders(order_id TEXT, customer_id TEXT);''')
    cursor.execute(
        '''INSERT INTO NewOrders SELECT order_id, customer_id FROM Orders;''')
    cursor.execute(
        '''ALTER TABLE Orders RENAME TO OrdersOriginal;''')
    cursor.execute(
        '''ALTER TABLE NewOrders RENAME TO Orders;''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS NewOrder_items(order_id TEXT,	order_item_id INTEGER, product_id TEXT,	seller_id TEXT);''')
    cursor.execute(
        '''INSERT INTO NewOrder_items SELECT order_id, order_item_id, product_id, seller_id FROM Order_items;''')
    cursor.execute(
        '''ALTER TABLE Order_items RENAME TO Order_itemsOriginal;''')
    cursor.execute(
        '''ALTER TABLE NewOrder_items RENAME TO Order_items;''')
    connection.commit()
    return


def scenario2():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = TRUE;')
    cursor.execute('''DROP TABLE Customers;''')
    cursor.execute('''ALTER TABLE CustomersOriginal RENAME TO Customers;''')
    cursor.execute('''DROP VIEW OrderSize;''')
    cursor.execute('''DROP TABLE Orders;''')
    cursor.execute('''ALTER TABLE OrdersOriginal RENAME TO Orders;''')
    cursor.execute('''DROP TABLE Order_items;''')
    cursor.execute(
        '''ALTER TABLE Order_itemsOriginal RENAME TO Order_items;''')
    connection.commit()
    return


# TODO: implement 3rd scenario
def scenario3():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = FALSE;')
    cursor.execute('CREATE INDEX Index1 On Orders (order_id,customer_id);')
    connection.commit()
    return


def main():
    global connection, cursor

    databases = [r"A3Small.db", r"A3Medium.db", r"A3Large.db"]

    times1 = []
    times2 = []
    times3 = []
    for db in databases:
        for i in range(3):
            connect(db)
            print("Connection to the " + db + " database open.")
            # setup appropriate scenario
            if i == 0:
                scenario1()
            elif i == 1:
                scenario2()
            else:
                scenario3()

            # start counting execution time
            start_time = time.time()
            result = []
            for x in range(5):
                result.append(query())

            if i == 0:
                times1.append((time.time() - start_time))
            elif i == 1:
                times2.append((time.time() - start_time))
            else:
                times3.append((time.time() - start_time))

            connection.close()
            print("Connection to the database closed.")
    print(times1)
    print(times2)
    print(times3)
    multi_bar_chart(times1, times2, times3, [
        "SmallDB", "MediumDB", "LargeDB"], "Query 2 Runtime (ms)")
    return


if __name__ == "__main__":
    main()
