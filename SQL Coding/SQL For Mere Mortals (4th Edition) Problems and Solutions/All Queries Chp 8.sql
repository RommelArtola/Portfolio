/*Sales Orders Database*/
--1: List customers and the dates they placed an order, sorted in order date sequence. (944)
SELECT CONCAT(CUSTLASTNAME, ', ', CUSTFIRSTNAME) AS CUST_NAME
		,OrderDate
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Customers AS CUSTOMER
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Orders AS ORDERS
	ON CUSTOMER.CUSTOMERID = ORDERS.CUSTOMERID
ORDER BY OrderDate;


--2: List employees and the customers for whom they booked an order. (211)
SELECT DISTINCT EMP.EmpFirstName
		,CUST.CustFirstName
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Orders AS ORD 
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Employees AS EMP
	ON ORD.EmployeeID = EMP.EmployeeID
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Customers AS CUST
	ON ORD.CustomerID  = CUST.CustomerID;


--3: Display all orders, the products in each order, and the amount owed for each product, in order number sequence. (3973)
SELECT Ordd.OrderNumber
		,Prod.ProductName
		,Ordd.QuotedPrice * Ordd.QuantityOrdered AS Amt_Owed
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Order_Details AS Ordd
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Products AS Prod
	ON Ordd.ProductNumber = Prod.ProductNumber
ORDER BY Ordd.OrderNumber;


--4: Show me the vendors and the products they supply to us for products that cost less than $100. (66)
SELECT Vend.VendName
		,Prod.ProductName
		,Prod.RetailPrice
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Product_Vendors AS PV
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Vendors AS Vend
	ON PV.VendorID = Vend.VendorID
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Products AS Prod
	ON PV.ProductNumber = Prod.ProductNumber
WHERE PV.WholesalePrice < 100;


--5: Show me customers and employees who have the same last name. (16)
SELECT Emp.EmpLastName, Cust.CustLastName
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Employees AS Emp
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Customers AS Cust
	ON Emp.EmpLastName = Cust.CustLastName;



--6: Show me customers and employees who live in the same city. (10)
SELECT Emp.EmpFirstName, Cust.CustFirstName, Emp.EmpCity
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Employees AS Emp
INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Customers AS Cust
	ON Emp.EmpCity = Cust.CustCity;



/*School Scheduling Database*/
--1: Display buildings and all the classrooms in each building. (47)
SELECT B.BuildingName
		,C.ClassRoomID
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Buildings AS B
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Class_Rooms AS C
	ON B.BuildingCode = C.BuildingCode;


--2: List students and all the classes in which they are currently enrolled. (50)
SELECT S.StudFirstName
		,C.ClassID
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Students AS S
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Student_Schedules AS SC
	ON S.StudentID = SC.StudentID
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Classes AS C
	ON SC.ClassID = C.ClassID
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Student_Class_Status AS SCS
	ON SC.ClassStatus = SCS.ClassStatus
	AND SCS.ClassStatusDescription = 'Enrolled';


--3: List the faculty staff and the subject each teaches. (110)
SELECT Stf.StfLastname
		,Sub.SubjectName
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Faculty_Subjects AS FC
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff AS Stf
	ON FC.StaffID = Stf.StaffID
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Subjects AS Sub
	ON Sub.SubjectID = FC.SubjectID;



--4: Show me the students who have a grade of 85 or better in art and who also have a grade of 85 or better in any computer course. (1)
SELECT Stud.StudFirstName
		,Stud.StudLastName
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Students AS Stud
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Student_Schedules AS SS
	ON Stud.StudentID = SS.StudentID
	AND SS.Grade >= 85
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Classes AS C
	ON SS.ClassID = C.ClassID
INNER JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Subjects AS Sub
	ON C.SubjectID = Sub.SubjectID
	AND Sub.SubjectName LIKE ('%ART%') AND 
		Sub.SubjectName LIKE ('%Computer%');



/*Entertainment Agency Database*/
--1: Display agents and the engagement dates they booked, sorted by booking start date. (111)
SELECT AgtFirstName
		,StartDate
		,EndDate
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Agents AS A
INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements AS E
	ON A.AgentID = E.AgentID;


--2: List customers and the entertainers they booked. (75)
SELECT DISTINCT C.CustFirstName
		,E.EntStageName
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements AS Book
INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Customers AS C
	ON Book.CustomerID = C.CustomerID
INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS E
	ON Book.EntertainerID = E.EntertainerID;


--3: Find the agents and entertainers who live in the same postal code. (10)
SELECT A.AgtFirstName 
		,E.EntStageName
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Agents AS A
INNER JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS E
	ON A.AgtZipCode = E.EntZipCode;