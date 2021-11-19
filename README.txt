README
Readme for Assignment 3

Names: Anushka Khare, Rachel Ellis, Elsa Xiaoyi Chen, Yi Meng Wang
CCIDs: anushka1, rjellis, xiaoyi9, yimeng2

We have consulted matplotlib documentation for stacked bar chart.

Query 1:

SELECT COUNT(*) 
FROM Customers C 
JOIN Orders ON C.customer_id 
WHERE C.customer_postal_code = random_postal_code

For the graphs presented for the first query it was found that for the all databases the time taken for uninformed scenario was less than the time taken for the self optimized scenario. This might be because the auto-indicies made based on the primary keys are not as effective as desired, and it could cause the query running time to be much longer. In this case, the results of user-optimized scenario was much lower as expected, since we are choosing the optimal indicies for the specific query, so the parsing through the data will be faster. 

For the useroptimized I created the specific index based on the postal code because we specifically want to take into consideration the group of and search through the postal code for the customers and then compare to the random postal code generated. 

Query 2:

For query 2, we executed the following query:
    CREATE VIEW IF NOT EXISTS OrderSize AS SELECT O.order_id as oid, COUNT(order_item_id) as size
	       FROM Orders as O, Order_items as I WHERE O.order_id = I.order_id GROUP BY O.order_id;
    SELECT AVG(size) FROM Customers as C, Orders as O, OrderSize WHERE C.customer_postal_code = :P
    AND C.customer_id = O.customer_id AND O.order_id = oid;

As displayed in the graph, the uninformed case takes the longest for each database. Additionally, these values are extremely larger than the other scenarios making their trend hard to observe. Compared to scenario 1, the other scenarios have relatively similar runtimes (compared to each other for the same database). By reviewing the time values used for the Q2A3chart.png plot, we can better observe the expected trend:

[58577.451944351196, 240946.6462135315, 1266324.550151825]

[391.06082916259766, 2169.227123260498, 12597.653150558472]

[209.41686630249023, 471.5592861175537, 2670.736074447632]

The numbers increase from left to right as we go from the smallDB to the largeDB. Also, decrease from top to down as we go from scenario 1 to 3. 

For the self-optimized scenario, we created two indices:
-  index on Customers (customer_postal_code) because we use this to match our randomly selected postal code. This operation is faster when we have an index for this attribute to group similar ones together, avoiding a scan through the entire table.
-  index on Orders (customer_id) since we are joining the Orders table to Customers using this attribute and grouping by this attribute on the Orders table speeds up the query


Query 3:

SELECT AVG(size) 
    FROM Customers as C, Orders as X, 
    (SELECT O.order_id, COUNT(order_item_id) as size
    FROM Orders as O, Order_items as I 
    WHERE O.order_id = I.order_id 
    GROUP BY O.order_id) as T
    WHERE C.customer_postal_code = random_postal_code
    AND T.order_id = X.order_id
    AND C.customer_id = X.customer_id

For each of the 3 databases, the uninformed case always took the longest time to output,  because linear scan without indices is slower for the most time. The self-optimized case took the similar amount of time to output as the user-optimized case, but only slightly slower, since user-optimized case chose to run on the optimal indices.

For each of the 3 databases, the uninformed case always took the longest time to output. The self-optimized case somehow took the similar amount of time to output as the user-optimized case, but only slightly slower. Since user-optimized case chose to run on the optimal indexes.

For query 3, I created the composite index on orders(order_id, customer_id), because both are the join column attributes in the query. Order_id is used to join table Orders and Order_items; customer_id joins table Customers and Orders.

For the graph for Q3, I chose to plot the y-axis using the log of time (I also confirmed this with my lab TA). Since using the original data, the uninformed case(blue column) took up the most space in the column and it was hard to observe the overall relationship between all 3 cases. The log of runtime provides a better comparison between these 3 cases.

Query 4:
For query 4, we executed the following query:

    SELECT COUNT(DISTINCT S.seller_postal_code) 
    FROM Order_items O, Sellers S 
    WHERE S.seller_id = O.seller_id AND O.order_id = 'random_order_id'

For all 3 databses, the uninformed case always took the longest time, then it is auto-indexed case, finally, the user-optimized case takes the shortest time. This result is expected; user-optimized makes the query faster since the manually created index is made to speed up this specific query. Linear scan is expected to be slower than mode without indicies, since there is no shortcuts to the search.

For this query, we created indicies on seller_id of Sellers, seller_id of Order_items, and order_id of Order_items. We decided to created these indicies because the query's conditions depend on these parameters. Creating indicies for seller_id in both tables allows it to quickly do the cartesian product for the two tables. Futhermore, the index for order_id allows it to quickly find the rows with desired order_id. 



