/*Sales Orders Database*/
-- 1: For each category of product, show me, by state, how much revenue the customers have generated. Give me subtotals for each state, for each category, plus a grand total. (35 rows)
SELECT CustState
		,CategoryDescription
		,SUM(QuotedPrice * QuantityOrdered) AS REVENUE_GENERATED

FROM SalesOrders.dbo.Order_Details AS OD

LEFT JOIN (SELECT C.CategoryID, ProductNumber, CategoryDescription
			FROM SalesOrders.dbo.Products AS P
			LEFT JOIN SalesOrders.dbo.Categories AS C
				ON P.CategoryID = C.CategoryID
		) PROD
	ON PROD.ProductNumber = OD.ProductNumber

LEFT JOIN (SELECT O.CustomerID, CustState, O.OrderNumber, CustLastName  + ', ' + CustFirstName AS CustName
			FROM SalesOrders.dbo.Customers AS C
			LEFT JOIN SalesOrders.dbo.Orders AS O
				ON C.CustomerID = O.CustomerID
			) AS CUST
	ON OD.OrderNumber = CUST.OrderNumber

GROUP BY CUBE (CustState, CategoryDescription)



-- 2: For each category of product, show me, by state, how much quantity the vendors have on hand. Give me subtotals for each state within a category, plus a grand total. (33 rows)
SELECT VendState
		,CategoryDescription
		,SUM(QuantityOnHand) AS TOT_ON_HAND_INV

FROM SalesOrders.dbo.Vendors AS V
LEFT JOIN SalesOrders.dbo.Product_Vendors AS PV
	ON V.VendorID = PV.VendorID
LEFT JOIN SalesOrders.dbo.Products AS P
	ON P.ProductNumber = PV.ProductNumber
LEFT JOIN SalesOrders.dbo.Categories AS C
	ON C.CategoryID = P.CategoryID
GROUP BY ROLLUP (CategoryDescription, VendState)




-- 3: For each of our vendors, let me know how many products they supply in each category. I want to see this broken down by state. For each state, show me the number of products in each category. Show me the number of products for all categories and a grand total as well. (43 rows)
	
SELECT VendState
		,CategoryDescription
		,COUNT(*) AS PROD_COUNT
	
FROM SalesOrders.dbo.Vendors AS V
INNER JOIN SalesOrders.dbo.Product_Vendors AS PV
	ON V.VendorID = PV.VendorID
INNER JOIN SalesOrders.dbo.Products AS P
	ON PV.ProductNumber = P.ProductNumber
INNER JOIN SalesOrders.dbo.Categories AS C
	ON P.CategoryID = C.CategoryID
GROUP BY 
	ROLLUP(V.VendState, C.CategoryDescription);
--Comment: I have no idea how he is getting 43 rows....



/*School Scheduling Database*/
-- 1: Summarize the number of class sessions scheduled, showing semester, building, classroom, and subject. Give me subtotals for each semester, for each combination of building and classroom and for each subject. (82 rows)
SELECT SemesterNumber
		,BuildingName
		,CR.ClassRoomID
		,SubjectName
		,COUNT(*) AS COUNTER
FROM SchoolScheduling.dbo.Classes AS C
LEFT JOIN SchoolScheduling.dbo.Class_Rooms AS CR
	ON C.ClassRoomID = CR.ClassRoomID
LEFT JOIN SchoolScheduling.dbo.Buildings AS B
	ON CR.BuildingCode = B.BuildingCode
LEFT JOIN (SELECT DISTINCT SubjectID, SubjectName 
			FROM SchoolScheduling.dbo.Subjects
			) AS S
	ON C.SubjectID = S.SubjectID
GROUP BY
	GROUPING SETS (SemesterNumber, BuildingName, CR.ClassRoomID, SubjectName)
--Once again, no clue how the author gets 82.



-- 2: For each department, show me the number of courses that could be offered, and whether they’re taught by a Professor, an Associate Professor, or an Instructor. Give me total courses per department and total courses overall as well. (20 rows)
SELECT DeptName
		,Title
		,COUNT(*) COURSES_OFFERED
		
FROM SchoolScheduling.dbo.Faculty AS F
INNER JOIN SchoolScheduling.dbo.Faculty_Subjects AS FS
	ON F.StaffID = FS.StaffID
INNER JOIN SchoolScheduling.dbo.Subjects AS S
	ON S.SubjectId = FS.SubjectID
INNER JOIN SchoolScheduling.dbo.Categories AS C
	ON S.CategoryID = C.CategoryID
INNER JOIN SchoolScheduling.dbo.Departments AS D
	ON D.DepartmentID = C.DepartmentID 

GROUP BY 
	ROLLUP(DeptName, Title)



-- 3: I want to know how many courses our students have been in contact with. Give me totals by whether they completed the course, are currently enrolled in it or withdrew. I’d also like to see this broken down by student major. May as well give me the total courses completed, enrolled and withdrawn while you’re at it. Don’t worry about splitting it up by semester. (26 rows)

SELECT ClassStatusDescription
		,Major
		,SUM(CASE WHEN ClassStatusDescription = 'Enrolled'	THEN 1 ELSE NULL END) AS ENROLLED_COUNT
		,SUM(CASE WHEN ClassStatusDescription = 'Completed' THEN 1 ELSE NULL END) AS COMPLETE_COUNT
		,SUM(CASE WHEN ClassStatusDescription = 'Withdrew'	THEN 1 ELSE NULL END) AS WITHDREW_COUNT
		,COUNT(*) AS TOTAL_COUNT

FROM SchoolScheduling.dbo.Student_Schedules AS SS
INNER JOIN SchoolScheduling.dbo.Student_Class_Status AS SCS
	ON SS.ClassStatus = SCS.ClassStatus
INNER JOIN SchoolScheduling.dbo.Students AS S
	ON S.StudentID = SS.StudentID
INNER JOIN SchoolScheduling.dbo.Majors AS M
	ON M.MajorID = S.StudMajor

GROUP BY
	GROUPING SETS (ClassStatusDescription, Major)
--I don't think I answered it how the author intended, but the question is definitely answered and easy to interpret, in my opinion... 







/*Entertainment Agency Database*/
-- 1: For each city where our entertainers live, show me how many different musical styles are represented. Give me totals for each combination of City and Style, for each City plus a grand total. (36 rows)
SELECT EntCity
		,StyleName
		,COUNT(*) AS STYLE_COUNTER
FROM Entertainment.dbo.Entertainers AS E
INNER JOIN Entertainment.dbo.Entertainer_Styles AS ES
	ON E.EntertainerID = ES.EntertainerID
INNER JOIN Entertainment.dbo.Musical_Styles AS MS
	ON ES.StyleID = MS.StyleID
GROUP BY 
	ROLLUP(EntCity, StyleName);




-- 2: For each city where our customers live, show me how many different musical styles they’re interested in. Give me total counts by city, total counts by style and total counts for each combination of city and style. (18 rows)
SELECT CustCity
		,StyleName
		,COUNT(*) AS STYLE_COUNTER
FROM Entertainment.dbo.Customers AS C
INNER JOIN Entertainment.dbo.Musical_Preferences AS MP
	ON C.CustomerID = MP.CustomerID
INNER JOIN Entertainment.dbo.Musical_Styles AS MS
	ON MP.StyleID = MS.StyleID
GROUP BY 
	GROUPING SETS(CustCity, StyleName, (CustCity, StyleName))
--Feel like this is one of his better written questions, and I think I performed as requested, but the row count is of?????




-- 3: Give me an analysis of all the bookings we’ve had. I want to see the number of bookings and the total charge broken down by the city the agent lives in, the city the customer lives in, and the combination of the two. (34 rows)
SELECT AgtCity
		,CustCity
		,SUM(ContractPrice) AS CONTRACT_CHARGE
		,COUNT(*) AS BOOKINGS_COUNT
FROM Entertainment.dbo.Engagements AS E
INNER JOIN Entertainment.dbo.Agents AS A
	ON E.AgentID = A.AgentID
INNER JOIN Entertainment.dbo.Customers AS C
	ON E.CustomerID = C.CustomerID
GROUP BY 
	GROUPING SETS (AgtCity, CustCity, (AgtCity, CustCity))
