/*Sales Orders Database*/
-- 1: Show me each vendor and the average by vendor of the number of days to deliver products that are greater than the average delivery days for all vendors. (5 rows)
SELECT VendName
		,AVG(DaysToDeliver) AS AVG_LEAD_TIME

FROM SalesOrders.dbo.Vendors AS V
INNER JOIN SalesOrders.dbo.Product_Vendors AS PV
	ON V.VendorID = PV.VendorID
GROUP BY VendName
HAVING AVG(DaysToDeliver) > (SELECT AVG(DaysToDeliver) FROM SalesOrders.dbo.Product_Vendors);



-- 2: Display for each product the product name and the total sales that is greater than the average of sales for all products in that category. (13 rows)
SELECT ProductName
	,SUM_GROSS_SALES
FROM (	SELECT P.CategoryID
			,P.ProductName
			,SUM(OD.QuotedPrice * OD.QuantityOrdered) AS SUM_GROSS_SALES
			,AVG(SUM(OD.QuotedPrice * OD.QuantityOrdered)) OVER (PARTITION BY P.CategoryID) AS AVG_CAT
		FROM SalesOrders.dbo.Products AS P
		INNER JOIN SalesOrders.dbo.Order_Details AS OD 
			ON OD.ProductNumber = P.ProductNumber 
		GROUP BY P.CategoryID, P.ProductName
	) AS SQ
WHERE SUM_GROSS_SALES > AVG_CAT;



-- 3: How many orders are for only one product? (1 row)
SELECT COUNT(FINAL.OrderNumber) AS ORDER_COUNT_WITH_SINGLE_PRODUCT
FROM (
		SELECT O.OrderNumber
			--,COUNT(*) AS SINGLE_PRODUCT_ORDER_COUNT 
		FROM SalesOrders.dbo.Orders AS O
		INNER JOIN SalesOrders.dbo.Order_Details AS OD
			ON O.OrderNumber = OD.OrderNumber
		GROUP BY O.OrderNumber
		HAVING COUNT(*) = 1
	) AS FINAL



/*School Scheduling Database*/
-- 1: Display by category the category name and the count of classes offered for those categories that have three or more classes. (14 rows)

SELECT CategoryDescription
	,COUNT(CAT.CategoryID) AS CATEGORY_COUNT
FROM SchoolScheduling.dbo.Categories AS CAT
INNER JOIN SchoolScheduling.dbo.Subjects AS SUB
	ON CAT.CategoryID = SUB.CategoryID
INNER JOIN SchoolScheduling.dbo.Classes AS CL
	ON SUB.SubjectID = CL.SubjectID
GROUP BY CategoryDescription
HAVING COUNT(CAT.CategoryID) >= 3
;


-- 2: List each staff member and the count of classes each is scheduled to teach for those staff members who teach fewer than three classes. (7 rows)   
SELECT StfLastname + ', ' + StfFirstName AS StfName
		,COUNT(FC.ClassID) AS STAFF_CLASS_COUNT
FROM SchoolScheduling.dbo.Staff AS S
LEFT JOIN SchoolScheduling.dbo.Faculty_Classes AS FC
	ON S.StaffID = FC.StaffID
GROUP BY StfLastname + ', ' + StfFirstName
HAVING COUNT(FC.ClassID) < 3

-- 3: Show me the subject categories that have fewer than three full professors teaching that subject. (16 rows)
SELECT CategoryDescription
		,COUNT(SQ.StaffID) AS STAFF_COUNT

FROM SchoolScheduling.dbo.Categories AS C
LEFT JOIN (SELECT CategoryID
					,FC.StaffID
			FROM SchoolScheduling.dbo.Faculty_Categories AS FC
			LEFT JOIN SchoolScheduling.dbo.Faculty AS F
				ON FC.StaffID = F.StaffID
			WHERE 0=0
			--AND Status = 'Full Time'
			AND F.Title = 'PROFESSOR'
			) AS SQ
	ON SQ.CategoryID = C.CategoryID
GROUP BY CategoryDescription
HAVING COUNT(SQ.StaffID) < 3




-- 4: Count the classes taught by every staff member. (27 rows)
SELECT S.StfLastname + ', ' + S.StfFirstName AS StfName
		,COUNT(ClassID) AS CLASS_COUNT
FROM SchoolScheduling.dbo.Staff AS S
LEFT JOIN SchoolScheduling.dbo.Faculty_Classes AS FC
	ON S.StaffID = FC.StaffID
GROUP BY S.StfLastname + ', ' + S.StfFirstName;




/*Entertainment Agency Database*/
-- 1: Show me the entertainers who have more than two overlapped bookings. (1 row)
SELECT EntStageName, EntertainerID
FROM Entertainment.dbo.Entertainers
WHERE EntertainerID IN (	SELECT E1.EntertainerID AS EntID
							FROM Entertainment.dbo.Engagements AS E1
							INNER JOIN Entertainment.dbo.Engagements AS E2
								ON E1.EntertainerID = E2.EntertainerID
								AND E1.EngagementNumber <> E2.EngagementNumber
								AND E1.StartDate <= E2.EndDate
								AND E2.Startdate <= E1.EndDate
							GROUP BY E1.EntertainerID
							HAVING COUNT(*) > 2
						);



-- 2: Show each agent’s name, the sum of the contract price for the engagements booked, and the agent’s total commission for agents whose total commission is more than $1,000. (4 rows)
WITH AGENT_DEETS AS (
	SELECT AgtFirstName + ', ' + AgtLastName AS AgtFullName
			,Salary
			,CommissionRate
			,AgentID
	FROM Entertainment.dbo.Agents 
) 

SELECT AgtFullName
		,SUM(ContractPrice) AS SUM_CONTRACT_PRICE
		,SUM(ContractPrice * CommissionRate) AS AGENT_GROSS_REV
FROM AGENT_DEETS AS AD
INNER JOIN Entertainment.dbo.Engagements AS E
	ON AD.AgentID = E.AgentID
GROUP BY AgtFullName
HAVING SUM(ContractPrice * CommissionRate) > 1000;