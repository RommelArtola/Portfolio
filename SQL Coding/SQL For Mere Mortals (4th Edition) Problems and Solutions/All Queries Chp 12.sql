/*Sales Orders Database*/
-- 1: What is the average retail price of a mountain bike? (1 row – value: $1321.25)
SELECT AVG(RetailPrice) AS Avg_Mtn_Bk_Retail_Price
FROM SalesOrders.dbo.Products
WHERE ProductName LIKE '%MOUNTAIN BIKE%';



-- 2: What was the date of our most recent order? (1 row – value: 2018-03-01).
SELECT MAX(ORDERDATE) AS MAX_ORDER_DT
FROM SalesOrders.dbo.Orders;


-- 3: What was the total amount for order number 8?  (1 row – value: $1492.60)
SELECT SUM(QuotedPrice * QuantityOrdered) AS TOT_REVENUE_ORDNUM_8
FROM SalesOrders.dbo.Order_Details
WHERE OrderNumber = 8;



/*School Scheduling Database*/
-- 1: What is the current average class duration? (1 row – value: 78.939 – but SQL Server truncates to 78)
SELECT AVG(Duration) AS AVG_CLASS_DURATION
FROM SchoolScheduling.dbo.Classes;


--2: List the last name and first name of each staff member who has been with us since the earliest hire date. (1 row – value: “Alborous, Sam”)
SELECT StfLastName, StfFirstName, DateHired
FROM SchoolScheduling.dbo.Staff
WHERE DateHired = (	SELECT MIN(DateHired) 
					FROM SchoolScheduling.dbo.Staff
				  );


-- 3: How many classes are held in room 3346? (1 row – value: 10)
SELECT COUNT(*) AS ROOM_3346_CLASS_COUNT
FROM SchoolScheduling.dbo.Classes
WHERE ClassRoomID = 3346;






/*Entertainment Agency Database*/
-- 1: What is the average salary of a booking agent?  (1 row – value: $24850.00)
SELECT AVG(SALARY) AS AGENT_AVG_SALARY
FROM Entertainment.dbo.Agents;



-- 2: Show me the engagement numbers for all engagements that have a contract price greater than or equal to the overall average contract price. (43 rows)
SELECT EngagementNumber
	,ContractPrice
FROM Entertainment.dbo.Engagements
WHERE ContractPrice >= (SELECT AVG(ContractPrice) 
						FROM Entertainment.dbo.Engagements
						);

-- 3: How many of our entertainers are based in Bellevue? (1 row – value: 3)
SELECT COUNT(*) AS ENTS_IN_BELLEVUE_COUNT
FROM Entertainment.dbo.Entertainers
WHERE EntCity = 'Bellevue';