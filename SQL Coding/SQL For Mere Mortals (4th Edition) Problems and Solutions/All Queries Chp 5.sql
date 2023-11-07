/*Sales Orders Database*/
--1: What if we adjusted each product price by reducing it 5 percent? (90)
SELECT PV.*
		,CAST(WholesalePrice * 0.95 AS NUMERIC(24,2)) AS Discounted_Price
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Product_Vendors AS PV;


--2: Show me a list of orders made by each customer in descending date order. (944)
SELECT CustomerID 
		,OrderDate
		,ShipDate
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Orders
ORDER BY OrderDate DESC, ShipDate DESC;



--3: Compile a complete list of vendor names and addresses in vendor name order. (10)
SELECT VendName
		,VendStreetAddress
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Vendors
ORDER BY VendName;








/*Entertainment Agency Database*/
--1: Give me the names of all our customers by city (15)
SELECT CustCity	
		,CustLastName
		,CustFirstName
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Customers
ORDER BY CustCity;



--2: List all entertainers and their Web sites. (13)
SELECT EntStageName
		,EntWebPage
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers
ORDER BY EntStageName;




--3: Show the date of each agent’s first six-month performance review. (9)
SELECT AgtLastName
		,AgtFirstName
		,DateHired
		,DATEADD(MONTH, 6, DateHired) AS First_Perfomance_Review
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Agents
ORDER BY DateHired;



/*School Scheduling Database*/
--1: Give me a list of staff members, and show them in descending order of salary. (27)
SELECT StfLastName
		,StfFirstName
		,Salary
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff
ORDER BY Salary DESC, StfLastname, StfFirstName;

--2: Can you give me a staff member phone list? (27)
SELECT StfLastName
		,StfFirstName
		,StfPhoneNumber
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff
ORDER BY StfLastname, StfFirstName;


--3: List the names of all our students, and order them by the cities they live in. (18)
SELECT StudCity
		,CONCAT(StudLastName, ', ', StudFirstName) AS StudName
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Students
ORDER BY StudCity;



/*Bowling League Database*/
--1: Show next year’s tournament date for each tournament location (20)
SELECT TourneyLocation
		,DATEADD(YEAR, 1, TourneyDate) AS Next_Tourney_Date
FROM OMSBA23_ARTOLA_BowlingLeagueExample.dbo.Tournaments
ORDER BY TourneyLocation;

--2: List the name and phone number for each member of the league. (32)
SELECT CONCAT(BowlerLastName, ', ', BowlerFirstName) AS BowlerName
	,BowlerPhoneNumber
FROM OMSBA23_ARTOLA_BowlingLeagueExample.dbo.Bowlers
ORDER BY BowlerLastName, BowlerFirstName;

--3: Give me a listing of each team’s lineup. (32)
SELECT TeamID
		,CONCAT(BowlerLastName, ', ', BowlerFirstName) AS BowlerName
FROM OMSBA23_ARTOLA_BowlingLeagueExample.dbo.Bowlers
ORDER BY TeamID;
