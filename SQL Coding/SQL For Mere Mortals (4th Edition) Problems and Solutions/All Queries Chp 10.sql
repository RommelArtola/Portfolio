










/*Sales Orders Database*/
-- 1: List the customers who ordered a helmet together with the vendors who provide helmets. (91)
SELECT DISTINCT CONCAT(CustLastName, ', ', CustFirstName) AS Name
		,ProductName
		, 1 AS IS_CUSTOMER
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Customers AS CUST
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Orders AS ORD
	ON CUST.CustomerID = ORD.CustomerID
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Order_Details AS OD
    ON OD.OrderNumber = ORD.OrderNumber
INNER JOIN  OMSBA23_ARTOLA_SalesOrdersExample.dbo.Products AS PROD
    ON PROD.ProductNumber = OD.ProductNumber
	AND PROD.ProductName LIKE '%Helmet%'

UNION ALL

SELECT VendName, ProductName, 0 AS IS_CUSTOMER
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Vendors AS V
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Product_Vendors AS PV
	ON V.VendorID = PV.VendorID 
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Products AS P
	ON PV.ProductNumber = P.ProductNumber
	AND P.ProductName LIKE '%HELMET%'
;



/*School Scheduling Database*/
-- 1: Create a mailing list for students and staff, sorted by ZIP Code. (45)
SELECT StudStreetAddress AS Address
		,StudZipCode AS ZipCode
		, 1 AS IS_STUDENT
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Students

UNION ALL

SELECT StfStreetAddress AS Address
		,StfZipCode AS ZipCode
		,0 AS IS_STUDENT
		
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff

ORDER BY 2, 1
;

/*Entertainment Agency Database*/
-- 1: Display a combined list of customers and entertainers. (28)
SELECT CONCAT(CustLastName, ', ', CustFirstName) AS Name
		,1 AS IS_CUSTOMER
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Customers

UNION

SELECT EntStageName
		,0 AS IS_CUSTOMER
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers



-- 2: Produce a list of customers who like contemporary music together with a list of entertainers who play contemporary music. (5)
SELECT CONCAT(CustLastName, ', ', CustFirstName) AS Name
		,1 AS IS_CUSTOMER
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Customers AS CUST
INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Musical_Preferences AS MP
	ON CUST.CustomerID = MP.CustomerID
	AND MP.StyleID IN (SELECT StyleID
						FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Musical_Styles
						WHERE StyleName LIKE '%CONTEMP%'
						)

UNION ALL

SELECT EntStageName
		,0 AS IS_CUSTOMER
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS ENT
INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainer_Styles AS ES
	ON ENT.EntertainerID = ES.EntertainerID
	AND ES.StyleID IN (SELECT StyleID
						FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Musical_Styles
						WHERE StyleName LIKE '%CONTEMP%'
						)