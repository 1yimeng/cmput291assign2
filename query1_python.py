import sqlite3
import time
from typing import Counter
import matplotlib.pyplot as plt
import random
import numpy as np
connection = None
cursor = None


def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def plotting(title, label1, values1, values2, values3):
    if len(values1) < 1 or len(values2) < 1 or len(values3) < 1:
        print('Warning: empty input so generated plot will be empty')
    width = 0.35
    fig, axis = plt.subplots()
    axis.bar(label1, values1, width, label="Uninformed")
    axis.bar(label1, values2, width, label="Self-Optimized",
             bottom=values1)  # stack
    axis.bar(label1, values3, width, label="User-Optimized",
             bottom=np.array(values2)+np.array(values1))

    # label x and y axis
    plt.xticks(range(len(label1)), label1)
    plt.legend()

    # give plot a title
    plt.title(title)

    # save plot to file
    # we'll use passed title to give file name
    path = './Q1A3chart.png'
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))

    # close figure so it doesn't display
    plt.close()
    return


def uninformed():
    global connection, cursor
    # turning off the autoindexing
    cursor.execute('PRAGMA automatic_index = FALSE;')
    # Customer Table
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS CustomersNew (customer_id TEXT, customer_postal_code INTEGER);''')
    cursor.execute(
        '''INSERT INTO CustomersNew SELECT customer_id, customer_postal_code FROM Customers;''')
    cursor.execute('''ALTER TABLE Customers RENAME TO CustomersOld;''')
    cursor.execute('''ALTER TABLE CustomersNew RENAME TO Customers;''')
    # Order Table
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS OrdersNew (order_id TEXT, customer_id TEXT);''')
    cursor.execute(
        '''INSERT INTO OrdersNew SELECT order_id, customer_id FROM Orders;''')
    cursor.execute('''ALTER TABLE Orders RENAME TO OrdersOld;''')
    cursor.execute('''ALTER TABLE OrdersNew RENAME TO Orders;''')
    connection.commit()
    return


def selfoptimized():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = TRUE;')
    # Customers Table
    cursor.execute('''DROP TABLE Customers;''')
    cursor.execute('''ALTER TABLE CustomersOld RENAME TO Customers;''')
    # Order Table
    cursor.execute('''DROP TABLE Orders;''')
    cursor.execute(''' ALTER TABLE OrdersOld RENAME TO Orders;''')
    connection.commit()
    return


def useroptimized():
    # need to define a specifc primary keys
    cursor.execute('PRAGMA automatic_index = FALSE;')
    # for Customer Table
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS CustomersNew (customer_id TEXT, customer_postal_code INTEGER);''')
    cursor.execute(
        '''INSERT INTO CustomersNew SELECT customer_id, customer_postal_code FROM Customers;''')
    cursor.execute('''ALTER TABLE Customers RENAME TO CustomersOld;''')
    cursor.execute('''ALTER TABLE CustomersNew RENAME TO Customers;''')

    # for Order Table
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS OrdersNew (order_id TEXT, customer_id TEXT);''')
    cursor.execute(
        '''INSERT INTO  OrdersNew SELECT order_id, customer_id FROM Orders;''')
    cursor.execute('''ALTER TABLE Orders RENAME TO OrdersOld;''')
    cursor.execute('''ALTER TABLE OrdersNew RENAME TO Orders;''')

    cursor.execute(
        '''CREATE INDEX IF NOT EXISTS IndexNew ON Customers(customer_id)''')
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS Index3 ON Customers(customer_postal_code)')
    return


def query_data():
    global connection, cursor

    # inputting the query for the database
    cursor.execute("""SELECT DISTINCT(customer_postal_code) from Customers""")
    random_rows = cursor.fetchall()
    rand_postal_code = random.choice(random_rows)
    cursor.execute(
        "SELECT COUNT(*) FROM Customers C JOIN Orders ON C.customer_id WHERE C.customer_postal_code = ?", (rand_postal_code))
    # getting all the outputs of the query
    #array_store = cursor.fetchone()[0]
    connection.commit()

    return


def main():
    global connection, cursor
    # running the uninformed scenario 50 times
    databases = [r"A3Small.db", r"A3Medium.db", r"A3Large.db"]

    times1 = []
    times2 = []
    times3 = []
    for db in databases:
        for i in range(1, 4):
            connect(db)
            print("Connection to the " + db + " database open.")

            if i == 1:
                uninformed()
            if i == 2:
                selfoptimized()
            if i == 3:
                useroptimized()

            # start counting execution time
            start_time = time.time()
            result = []
            for x in range(50):
                query_data()

            if i == 1:
                times1.append((time.time() - start_time)*1000)
            if i == 2:
                times2.append((time.time() - start_time)*1000)
            if i == 3:
                times3.append((time.time() - start_time)*1000)

            connection.close()
            print("Connection to the database closed.")
            print(times1)
            print(times2)
            print(times3)
    plotting("Runtime for Query 1 in ms", [
        "SmallDB", "MediumDB", "LargeDB"], times1, times2, times3)
    return


if __name__ == "__main__":
    main()
