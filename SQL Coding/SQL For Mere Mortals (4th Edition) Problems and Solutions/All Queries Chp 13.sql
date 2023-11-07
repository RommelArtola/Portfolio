/*Sales Orders Database*/
-- 1: Show me each vendor and the average by vendor of the number of days to deliver products. (10 rows)
SELECT V.VendName
	,AVG(DaysToDeliver) AS AVG_VEND_LEAD_TIME
FROM SalesOrders.dbo.Product_Vendors AS PV
LEFT JOIN SalesOrders.dbo.Vendors AS V
	ON PV.VendorID = V.VendorID
GROUP BY V.VendName;


-- 2: Display for each product the product name and the total sales. (38 rows)
SELECT ProductName
		,SUM(QuotedPrice * QuantityOrdered) AS SUM_REVENUE_GENERATED
FROM SalesOrders.dbo.Products AS P
LEFT JOIN SalesOrders.dbo.Order_Details AS OD
	ON P.ProductNumber = OD.ProductNumber
WHERE QuantityOrdered IS NOT NULL
GROUP BY ProductName;



-- 3: List all vendors and the count of products sold by each. (10 rows)
SELECT VendName
		,COUNT(ProductNumber) AS PRODUCTS_SOLD_COUNT
FROM SalesOrders.dbo.Product_Vendors AS PV
LEFT JOIN SalesOrders.dbo.Vendors AS V
	ON PV.VendorID = V.VendorID
GROUP BY VendName;



-- 4: Challenge: Now solve problem 3 by using a subquery (10 rows)
SELECT VEND_DEETS.VendName
		,VEND_AVG.PRODUCTS_SOLD_COUNT
FROM (
		SELECT VendorID
				,COUNT(ProductNumber) AS PRODUCTS_SOLD_COUNT
		FROM SalesOrders.dbo.Product_Vendors AS PV
		GROUP BY VendorID
	) VEND_AVG
LEFT JOIN (SELECT VendorID, VendName
			FROM SalesOrders.dbo.Vendors AS V
		  ) AS VEND_DEETS
ON VEND_AVG.VendorID = VEND_DEETS.VendorID;





/*School Scheduling Database*/
-- 1: Display by category the category name and the count of classes offered. (15 rows)
SELECT C.CategoryDescription
		,COUNT(S.SubjectID) AS CLASS_COUNT
FROM SchoolScheduling.dbo.Categories AS C
INNER JOIN SchoolScheduling.dbo.Subjects AS S
	ON C.CategoryID = S.CategoryID
INNER JOIN SchoolScheduling.dbo.Classes AS CL
	ON S.SubjectID = CL.SubjectID
GROUP BY C.CategoryDescription;



-- 2: List each staff member and the count of classes each is scheduled to teach. (22 rows) 			
SELECT StfLastname + ', ' + StfFirstName AS StfName
		,COUNT(FC.ClassID) AS CLASS_COUNT
FROM SchoolScheduling.dbo.Staff AS S
INNER JOIN SchoolScheduling.dbo.Faculty_Classes AS FC
	ON S.StaffID = FC.StaffID
GROUP BY StfLastname + ', ' + StfFirstName




-- 3: Challenge: Now solve problem 2 by using a subquery. (27 rows)
SELECT StfLastname + ', ' + StfFirstName AS StfName
		,CLASS_COUNT
FROM SchoolScheduling.dbo.Staff AS S
LEFT JOIN (SELECT StaffID
				,COUNT(ClassID) AS CLASS_COUNT
			FROM SchoolScheduling.dbo.Faculty_Classes AS FC
			GROUP BY StaffID
			) AS SC
ON S.StaffID = SC.StaffID



-- 4: Can you explain why the subquery solution returns five more rows? Is it possible to modify the query in question 2 to return 27 rows? If so, how would you do it?
SELECT StfLastname + ', ' + StfFirstName AS StfName
		,COUNT(FC.ClassID) AS CLASS_COUNT
FROM SchoolScheduling.dbo.Staff AS S
LEFT JOIN SchoolScheduling.dbo.Faculty_Classes AS FC
	ON S.StaffID = FC.StaffID
GROUP BY StfLastname + ', ' + StfFirstName;

-- Answer: Yes. 5 Teachers aren't teaching any classes. Using left join instead of full join. Full join can result in unpredictable results. Though it really depends on how you structure the subquery more than just because it's a subquery.



/*Entertainment Agency Database*/
-- 1: Show each agent’s name, the sum of the contract price for the engagements booked, and the agent’s total commission. (8 rows)
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