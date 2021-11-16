import sqlite3
import matplotlib.pyplot as plt

connection = None
cursor = None


def multi_bar_chart(values1, values2, values3, labels, title):
    # if lists empty print warning
    if len(values1) < 1 or len(values2) < 1 or len(values3) < 1:
        print('Warning: empty input so generated plot will be empty')

    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(labels, values1, width, label="Uninformed")
    ax.bar(labels, values2, width, label="Self-Optimized")
    ax.bar(labels, values3, width, label="User-Optimized")

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
    # TODO: randomly pick postal code
    postalCode = 1
    cursor.execute("""CREATE VIEW IF NOT EXISTS OrderSize AS SELECT O.order_id as oid, COUNT(order_item_id) as size
	            FROM Orders as O, Order_items as I WHERE O.order_id = I.order_id GROUP BY O.order_id;

    SELECT AVG(size) FROM Customers as C, Orders as O, OrderSize WHERE customer_postal_code = :P
    AND C.customer_id = O.customer_id AND O.order_id = oid;""", {"P": postalCode})

    # get result
    result = cursor.fetchone()[0]
    connection.commit()
    return result


def scenario1():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = FALSE;')
    cursor.execute('''CREATE TABLE NewCustomers (customer_id TEXT, customer_postal_code INTEGER);
    INSERT INTO NewCustomers SELECT customer_id, customer_postal_code FROM Customers;
    ALTER TABLE Customers RENAME TO CustomersOriginal; 
    ALTER TABLE NewCustomers RENAME TO Customers;
    
    CREATE TABLE NewOrders (order_id TEXT, customer_id TEXT);
    INSERT INTO NewOrders SELECT order_id, customer_id FROM Orders;
    ALTER TABLE Orders RENAME TO OrdersOriginal; 
    ALTER TABLE NewOrders RENAME TO Orders;
    
    CREATE TABLE NewOrder_items (order_id TEXT,	order_item_id INTEGER, product_id TEXT,	seller_id TEXT);
    INSERT INTO NewOrder_items SELECT order_id, order_item_id, product_id, seller_id FROM Order_items;
    ALTER TABLE Order_items RENAME TO Order_itemsOriginal; 
    ALTER TABLE NewOrder_items RENAME TO Order_items;''')
    connection.commit()
    return


def scenario2():
    global connection, cursor
    cursor.execute('PRAGMA automatic_index = TRUE;')
    cursor.execute('''DROP TABLE Customers;
        ALTER TABLE CustomersOriginal RENAME TO Customers;  
        DROP TABLE Orders;
        ALTER TABLE OrdersOriginal RENAME TO Orders;  
        DROP TABLE Orders_items;
        ALTER TABLE Orders_itemsOriginal RENAME TO Orders_items;''')
    connection.commit()
    return


# TODO: implement 3rd scenario
def scenario3():
    return


def main():
    global connection, cursor

    databases = ["./A3Small", "./A3Medium", "./A3Large"]

    times1 = []
    times2 = []
    times3 = []
    for db in databases:
        connect(db)
        print("Connection to the database open.")

        for i in range(3):
            # setup appropriate scenario
            if i == 0:
                scenario1()
            elif i == 1:
                scenario2()
            else:
                scenario3()

            # TODO: start counting execution time
            result = []
            for i in range(50):
                result.append(query())

            connection.close()
            print("Connection to the database closed.")

    multi_bar_chart(times1, times2, times3, [
                    "SmallDB", "MediumDB", "LargeDB"], "Query 2 Runtime (ms)")
    return


if __name__ == "__main__":
    main()
