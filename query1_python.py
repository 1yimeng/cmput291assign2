import sqlite3
import time
from typing import Counter


connection = None
cursor = None


def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def uninformed():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = FALSE;')
    cursor.execute('''CREATE TABLE NewCustomers (customer_id TEXT, customer_postal_code INTEGER);
    INSERT INTO NewCustomers SELECT customer_id, customer_postal_code FROM Customers;
    ALTER TABLE Customers RENAME TO CustomersOld; 
    ALTER TABLE NewCustomers RENAME TO Customers;
    
    CREATE TABLE NewOrders (order_id TEXT, customer_id TEXT);
    INSERT INTO NewOrders SELECT order_id, customer_id FROM Orders;
    ALTER TABLE Orders RENAME TO OrdersOriginal; 
    ALTER TABLE NewOrders RENAME TO Orders;''')
    connection.commit()
    return


def selfoptimized():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = TRUE;')
    cursor.execute('''DROP TABLE Customers;
        ALTER TABLE CustomersOld RENAME TO Customers;  
        DROP TABLE Orders;
        ALTER TABLE OrdersOld RENAME TO Orders;''')
    connection.commit()
    return


def useroptimized():
    # need to define a specifc primary keys
    cursor.execute('CREATE INDEX Index1 ON Customers(customer_id)')
    cursor.execute('CREATE INDEX Index1 ON Customers(customer_postal_code)')
    return


def query_data():
    global connection, cursor
    # inputting the query for the database
    cursor.execute('''SELECT count(*)
FROM Customers C, Orders O
JOIN C.customer_id ON O.customer_id
WHERE rand_postal_code = C.customer_postal_code ''',
                   )
    # getting all the outputs of the query
    array_store = cursor.fetchall()
    connection.commit()

    return array_store


def main():
    global connection, cursor
    # running the uninformed scenario 50 times
    databases = [r"A3Small.db", r"A3Medium.db", r"A3Large.db"]

    times1 = []
    times2 = []
    times3 = []
    for db in databases:
        for i in range(3):
            connect(db)
            print("Connection to the " + db + " database open.")
            # setup appropriate scenario
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
                result.append(query_data())

            if i == 1:
                times1.append((time.time() - start_time))
            if i == 2:
                times2.append((time.time() - start_time))
            if i == 3:
                times3.append((time.time() - start_time))

            connection.close()
            print("Connection to the database closed.")
    print(times1)
    print(times2)
    print(times3)
    return

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
