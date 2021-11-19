README
Readme for Assignment 3

Names: Anushka Khare, Rachel Ellis, Elsa Xiaoyi Chen
CCIDs: anushka1, rjellis, xiaoyi9

We declare that we did not collaborate with anyone in this assignment outside of our group

General Assumption: 
Also while coding the user-optimized scenario, primary keys were not explicitly declared since when we did this as per our analysis using EXPLAIN QUERY PLAN function in the SQLite. Upon analysis we observed that if we passed the primary key then DB automtaically used those as index rather than the indexes specified later on. In order to avoid this issue we decided not to specify the primary key (simulate scenario 1 and then creating our own keys).

Query 1:

For the graphs presented for the first query it was found that for the A3Small database the time taken for uninformed scenario 
was less than the time taken for the Self Optimized scenario. This could be due to the fact that for a linear scan could be more optimized
if the parsing based on the primary keys is worse than a scanning the database. In this case the results of useroptimized scenario was much lower
as expected, since we are choosing the optimal indexes for the specific query, so the parsing through the data will be faster. 

For the A3Medium, the results are as expected, the uninformed scenario takes longer to read than the self optimized scenario. This is also because the self optimized will use primary keys as therefore it will run faster. Also the useroptimzed scenarios will run faster than the other two scenarios because the indexes are running on indexes that are specialized for that specific query

For the A3Large, the results are as expected, the uninformed scenario takes longer to read than the self optimized scenario. This is also 
because the self optimized will use primary keys as therefore it will run faster. Also the useroptimzed scenarios will run faster than the other two scenarios because the indexes are running on indexes that are specialized for that specific query

Query 2:

As displayed in the graph, the uninformed case takes the longest for each database. Additionally, these values are extremely larger than the other scenarios making their trend hard to observe. Compared to scenario 1, the other scenarios have relatively similar runtimes (compared to each other for the same database). By reviewing the time values used for the Q2A3chart.png plot, we can better observe the expected trend:

[71315.99450111389, 278797.4145412445, 2259579.808950424]

[390.44976234436035, 1012.0851993560791, 3468.294620513916]

[407.45091438293457, 982.8619956970215, 2062.3245239257812]

The numbers increase from left to right as we go from the smallDB to the largeDB. Also, decrease from top to down as we go from scenario 1 to 3. 

For the self-optimized scenario, we created two indices:
-  index on Customers (customer_postal_code) because we use this to match our randomly selected postal code. This operation is faster when we have an index for this attribute to group similar ones together, avoiding a scan through the entire table.
-  composite index on Orders (order_id,customer_id) since we are joining the Orders table to Customers and the View using those attributes. Note, from tests in DB Browser I confirmed that this is the correct order of the attributes (the other way around doesn't work). 


Query 3:
For each of the 3 databases, the uninformed case always took the longest time to output. The self-optimized case somehow took the similar amount of time to output as the user-optimized case, but only slightly slower. Since user-optimized case chose to run on the optimal indexes.

For query 3, I created the composite index on orders(order_id, customer_id), because both are the join column attributes in the query. Order_id is used to join table Orders and Order_items; customer_id joins table Customers and Orders.

For the graph for Q3, initialy I got the similar plot as Q2. Then, I chose to plot the y-axis using the log of time (I also confirmed this with my lab TA). Since using the original data, the uninformed case(blue column) took up the most space in the column and it was hard to observe the overall relationship between all 3 cases. The log of runtime provides a better comparison between these 3 cases.
