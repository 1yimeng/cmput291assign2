README
Readme for Assignment 3

Names: Anushka Khare, Rachel Ellis
CCIDs: anushka1, rjellis

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



