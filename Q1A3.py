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
    bottoms = [a+b for a,b in zip(values1, values2)]
    axis.bar(label1, values1, width, label="Uninformed")
    axis.bar(label1, values2, width, label="Self-Optimized",
             bottom=values1)  # stack
    axis.bar(label1, values3, width, label="User-Optimized",
             bottom=bottoms)

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
    cursor.execute('PRAGMA automatic_index = FALSE')
    # Customer Table
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS CustomersNew (customer_id TEXT, customer_postal_code INTEGER)''')
    cursor.execute(
        '''INSERT INTO CustomersNew SELECT customer_id, customer_postal_code FROM Customers''')
    cursor.execute('''ALTER TABLE Customers RENAME TO CustomersOld''')
    cursor.execute('''ALTER TABLE CustomersNew RENAME TO Customers''')
    # Order Table
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS OrdersNew (order_id TEXT, customer_id TEXT)''')
    cursor.execute(
        '''INSERT INTO OrdersNew SELECT order_id, customer_id FROM Orders''')
    cursor.execute('''ALTER TABLE Orders RENAME TO OrdersOld''')
    cursor.execute('''ALTER TABLE OrdersNew RENAME TO Orders''')
    connection.commit()
    return


def undo_uninformed():
    global connection, cursor
    # Customers Table
    cursor.execute('''DROP TABLE Customers''')
    cursor.execute('''ALTER TABLE CustomersOld RENAME TO Customers''')
    # Order Table
    cursor.execute('''DROP TABLE Orders''')
    cursor.execute('''ALTER TABLE OrdersOld RENAME TO Orders''')
    connection.commit()
    return

def random_customer_postal():
    cursor.execute("""SELECT DISTINCT(customer_postal_code) from Customers""")
    random_rows = cursor.fetchall()
    return random_rows

def query_data():
    global connection, cursor

    # inputting the query for the database
    all_random = random_customer_postal()
    start = time.time()
    all_postals = []
    for i in range(50):
        all_postals.append(random.choice(all_random))
    for i in range(50):
        cursor.execute(
            "SELECT COUNT(*) FROM Customers C JOIN Orders ON C.customer_id WHERE C.customer_postal_code = ?", (all_postals[i]))
    end = time.time()
    result = end - start
    connection.commit()
    return result


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
            # print("Connection to the " + db + " database open.")

            if i == 1:
                uninformed()
                result = query_data()
                undo_uninformed()
            if i == 2:
                cursor.execute('PRAGMA automatic_index = TRUE')
                result = query_data()
            if i == 3:
                cursor.execute(
                'CREATE INDEX IF NOT EXISTS Index3 ON Customers(customer_postal_code)')
                result = query_data()

            if i == 1:
                times1.append(result*1000)
            if i == 2:
                times2.append(result*1000)
            if i == 3:
                times3.append(result*1000)

            connection.close()
            # print("Connection to the database closed.")
    print(times1)
    print(times2)
    print(times3)
    plotting("Runtime for Query 1 in ms", [
        "SmallDB", "MediumDB", "LargeDB"], times1, times2, times3)
    return


if __name__ == "__main__":
    main()
