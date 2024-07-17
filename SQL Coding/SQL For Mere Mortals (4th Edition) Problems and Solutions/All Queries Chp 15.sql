/*Sales Orders Database*/
USE SalesOrders
-- 1: Apply a 5 percent discount to all orders for customers who purchased more than $50,000 in the month of October 2017. (639 changed)
--UPDATE Order_Details
SET QuotedPrice = ROUND(QuotedPrice * .95, 2)
WHERE 0=0
AND OrderNumber IN ( SELECT O.OrderNumber
						FROM Orders AS O
						WHERE O.CustomerID IN (SELECT O.CustomerID--, SUM(QuotedPrice * QuantityOrdered) AS SUM_QUOTED
												FROM Order_Details AS OD
												INNER JOIN Orders AS O
													ON OD.OrderNumber = O.OrderNumber
												WHERE YEAR(O.OrderDate) = 2017 AND MONTH(O.OrderDate) = 10
												GROUP BY O.CustomerID
												HAVING SUM(QuotedPrice * QuantityOrdered) > 50000
												)
						);

SELECT * 
FROM Order_Details
WHERE OrderNumber = 23 AND ProductNumber = 11;
--Before = 1650
--After = 1567.50

	
	
-- 2: Set the retail price of accessories (category = 1) to the wholesale price of the highest-priced vendor plus 35 percent (11 rows changed)
--UPDATE PRODUCTS
SET RetailPrice = CAST(ROUND(1.35*(SELECT MAX(WholesalePrice)
						  FROM Product_Vendors AS PV 
						  WHERE Products.ProductNumber = PV.ProductNumber
						  )
					,0) AS DECIMAL(10,2))
WHERE RetailPrice < (SELECT MAX(WholesalePrice) * 1.35
					FROM Product_Vendors AS PV
					WHERE Products.ProductNumber = PV.ProductNumber
					)
AND CategoryID = 1



SELECT *
FROM Products
WHERE CategoryID = 1 AND ProductNumber = 3
--Was 75 before. 
--After: 77.00


/*School Scheduling Database*/
USE SchoolScheduling
-- 1: Increase the salary of full-time tenured staff by 5 percent (21 rows changed).
--UPDATE Staff
SET Salary = 1.05 * (SELECT Salary
		FROM Faculty
		WHERE Staff.StaffID = Faculty.StaffID
		AND Status = 'Full Time' AND Tenured = 1
		)
WHERE (SELECT Salary
		FROM Faculty
		WHERE Staff.StaffID = Faculty.StaffID
		AND Status = 'Full Time' AND Tenured = 1
		) IS NOT NULL




SELECT * 
FROM Staff
WHERE StaffID = 98019
--Before: 45,000
--After: 47,250


-- 2: For all staff in zip codes 98270 and 98271, change the area code to 360 (2 rows changed).
USE SchoolSchedulingM
UPDATE Staff
SET StfAreaCode = CAST(360 AS VARCHAR(5))
WHERE StfZipCode IN ('98270', '98271');





/*Entertainment Agency Database*/
USE Entertainment
-- 1: Apply a 2 percent discount to all engagements for customers who booked more than $3,000 worth of business in the month of October 2017. (34 rows changed)

UPDATE Engagements
SET ContractPrice = 0.98 * ContractPrice
WHERE CustomerID IN (SELECT Engagements.CustomerID--, SUM(ContractPrice) AS TOT_PRICE
					 FROM Engagements 
					 WHERE 0=0
					  AND ( (YEAR(StartDate) = 2017 AND MONTH(StartDate) = 10) OR
					  (YEAR(EndDate) = 2017 AND MONTH(EndDate) = 10)
						  )
					  GROUP BY Engagements.CustomerID
					   HAVING SUM(ContractPrice) > 3000
						)






-- 2: Add 0.5 percent to the commission rate of agents who have sold more than $20,000 in engagements.(3 rows changed)
UPDATE Agents
SET CommissionRate = CommissionRate + 0.5
WHERE AgentID IN (SELECT AgentID--, SUM(ContractPrice) AS SUM_PRICE
				  FROM Engagements
				  GROUP BY AgentID
				  HAVING SUM(ContractPrice) > 20000
				  )


