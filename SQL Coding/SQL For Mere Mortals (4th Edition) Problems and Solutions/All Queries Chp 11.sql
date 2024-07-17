




















/*Sales Orders Database*/
-- 1: Display products and the latest date each product was ordered. (40) 
SELECT P.ProductName
		,MAX_ORD_DT

FROM OMSBA23_ARTOLA_SalesORdersExample.dbo.Products AS P
LEFT JOIN (SELECT ProductNumber, MAX(OrderDate) AS MAX_ORD_DT
			FROM OMSBA23_ARTOLA_SalesORdersExample.dbo.Order_Details AS OD
			LEFT JOIN OMSBA23_ARTOLA_SalesORdersExample.dbo.Orders AS ORD
				ON OD.OrderNumber = ORD.OrderNumber
			GROUP BY ProductNumber
			) AS PDT
ON P.ProductNumber = PDT.ProductNumber;
-- Q: Do you see any blank dates in the result?  Can you explain why?)
-- A: Yes, products that have never been order, and thus don't have a max order date.





-- 2: List customers who ordered bikes. (23)
SELECT CONCAT(CustLastName, ', ', CustFirstName) AS CustName
FROM OMSBA23_ARTOLA_SalesORdersExample.dbo.Customers AS CUST
INNER JOIN (SELECT DISTINCT CustomerID
			FROM OMSBA23_ARTOLA_SalesORdersExample.dbo.Orders AS ORD
			INNER JOIN OMSBA23_ARTOLA_SalesORdersExample.dbo.Order_Details AS OD
				ON ORD.OrderNumber = OD.OrderNumber
			INNER JOIN OMSBA23_ARTOLA_SalesORdersExample.dbo.Products AS PROD
				ON OD.ProductNumber = PROD.ProductNumber
				AND PROD.CategoryID IN ( SELECT CategoryID
										 FROM OMSBA23_ARTOLA_SalesORdersExample.dbo.Categories
										 WHERE CategoryDescription = 'Bikes'
										) 
			) AS BIKE_ORDS
	ON CUST.CustomerID = BIKE_ORDS.CustomerID
;


-- 3: What products have never been ordered? (2)
SELECT ProductName
FROM OMSBA23_ARTOLA_SalesORdersExample.dbo.Products
WHERE ProductNumber NOT IN (SELECT ProductNumber
							FROM OMSBA23_ARTOLA_SalesORdersExample.dbo.Order_Details
							);
-- This could've just also been answered with the 1st question using MAX_ORD_DT IS NULL....





/*School Scheduling Database*/
-- 1: List all staff members and the count of classes each teaches. (27)
SELECT DISTINCT S.StaffID 
		,COUNT(FC.ClassID) AS CLASS_COUNT
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff AS S
LEFT JOIN  OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Faculty_Classes AS FC
	ON S.StaffID = FC.StaffID
GROUP BY S.StaffID;



-- 2: Display students enrolled in a class on Tuesday. (18)
SELECT DISTINCT StudentID
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Student_Schedules 
WHERE ClassID IN (	SELECT ClassID
					FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Classes
					WHERE ThursdaySchedule = 1
					)


-- 3: List the subjects taught on Wednesday. (34)
SELECT SubjectName
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Subjects
WHERE SubjectID IN (SELECT SubjectID
					FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Classes
					WHERE WednesdaySchedule = 1
					);




/*Entertainment Agency Database*/
-- 1: Show me all entertainers and the count of each entertainer’s engagements. (13)
SELECT ENT.EntertainerID
	,COUNT(EngagementNumber) ENG_COUNT
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS ENT
LEFT JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements AS ENG
	ON ENT.EntertainerID = ENG.EntertainerID
GROUP BY ENT.EntertainerID;



-- 2: List customers who have booked entertainers who play country or country rock. (13)
SELECT DISTINCT CUST.CustomerID
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Customers AS CUST
INNER JOIN (SELECT CustomerID
			FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements AS ENG
			INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS ENT
				ON ENG.EntertainerID = ENT.EntertainerID
			INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainer_Styles AS ES
				ON ENG.EntertainerID = ES.EntertainerID
				AND ES.StyleID IN (	SELECT StyleID
									FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Musical_Styles
									WHERE StyleName IN ('Country', 'Country Rock')
								)
		) AS ENG
ON CUST.CustomerID = ENG.CustomerID;


-- 3: Find the entertainers who played engagements for customers Berg or Hallmark. (8)
SELECT DISTINCT EntStageName
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS ENT
INNER JOIN (SELECT ENT.EntertainerID 
			FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS ENT
			INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements AS ENG
				ON ENT.EntertainerID = ENG.EntertainerID
				AND ENG.CustomerID IN (	SELECT CustomerID
										FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Customers AS CUST
										WHERE CustLastName IN ('Hallmark', 'Berg')
									)
		) AS ENG
ON ENT.EntertainerID = ENG.EntertainerID





-- 4: Display agents who haven’t booked an entertainer. (1)
SELECT DISTINCT AgtLastName, AgtFirstName
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Agents
WHERE AgentID NOT IN (	SELECT AgentID
						FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements
					);