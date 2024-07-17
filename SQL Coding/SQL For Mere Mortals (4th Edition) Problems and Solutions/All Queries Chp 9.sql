/*Sales Orders Database*/
--1: Show me customers who have never ordered a helmet. (3)

SELECT Cust.CustFirstName
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Customers AS Cust
WHERE Cust.CustomerID NOT IN (
				SELECT DISTINCT CustomerID
				FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Products AS Prod
				INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Order_Details AS OD
					ON Prod.ProductNumber = OD.ProductNumber
				INNER JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Orders AS O
					ON O.OrderNumber = OD.OrderNumber
				WHERE Prod.ProductName LIKE '%HELMET'
				);

--2: Display customers who have no sales rep (employees) in the same ZIP Code. (18)
SELECT DISTINCT Cust.CustFirstName
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Customers AS Cust
LEFT JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Employees AS Emp
	ON Cust.CustZipCode = Emp.EmpZipCode
WHERE Emp.EmpZipCode IS NULL;

--3: List all products and the dates for any orders. (2681)
SELECT DISTINCT Prod.ProductName, O.OrderDate
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Products AS Prod
FULL JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Order_Details AS OD
	ON Prod.ProductNumber = OD.ProductNumber
LEFT JOIN OMSBA23_ARTOLA_SalesOrdersExample.dbo.Orders	AS O
	ON OD.OrderNumber = O.OrderNumber;


/*School Scheduling Database*/
--1: Show me classes that have no students enrolled. (118)
SELECT Class.ClassID
		,StSch.StudentID
FROM  OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Classes AS Class
LEFT JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Student_Schedules AS StSch
	ON Class.ClassID = StSch.ClassID
	AND StSch.ClassStatus IN (	SELECT ClassStatus
								FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Student_Class_Status
								WHERE ClassStatusDescription = 'Enrolled'
								)
WHERE StSch.StudentID IS NULL
ORDER BY Class.ClassID;


--2: Display subjects with no faculty assigned. (1)
SELECT Fac.StaffID, Sub.SubjectID, Sub.SubjectName, Sub.SubjectDescription
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Faculty_Subjects AS FS
FULL JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Faculty AS Fac
	ON FS.StaffID = Fac.StaffID
FULL JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Subjects AS Sub
	ON FS.SubjectID = Sub.SubjectID
WHERE Fac.StaffID IS NULL;
							

--3: List students not currently enrolled in any classes. (2)
SELECT Stud.StudentId
		,Stud.StudLastName + ', ' + Stud.StudFirstName AS StudName
FROM SchoolScheduling.dbo.Students AS Stud
WHERE Stud.StudentId NOT IN (SELECT SS.StudentId
							FROM SchoolScheduling.dbo.Student_Class_Status AS SCS
							INNER JOIN SchoolScheduling.dbo.Student_Schedules AS SS
								ON SCS.ClassStatus = SS.ClassStatus
							WHERE ClassStatusDescription = 'Enrolled'
							);


--4: Display all faculty and the classes they are scheduled to teach. (135)
SELECT Staff.StaffID, Staff.StfFirstName, Class.ClassID
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff AS Staff
LEFT JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Faculty_Classes AS FC
	ON Staff.StaffID = FC.StaffID
LEFT JOIN OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Classes AS Class
	ON FC.ClassID = Class.ClassID


/*Entertainment Agency Database*/
--1: Display agents who haven’t booked an entertainer. (1)
SELECT Ag.AgentID, Ag.AgtFirstName
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Agents AS Ag
WHERE Ag.AgentID NOT IN (SELECT DISTINCT AgentID
						 FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements
						 )



--2: List customers with no bookings. (2)
SELECT Cus.CustomerID, Cus.CustFirstName, Eng.EngagementNumber
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Customers AS Cus
LEFT JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements AS Eng
	ON Cus.CustomerID = Eng.CustomerID
WHERE Eng.CustomerID IS NULL;



--3: List all entertainers and any engagements they have booked. (112)
SELECT Ent.EntertainerID
		,Ent.EntStageName
		,Eng.EngagementNumber
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Entertainers AS Ent
LEFT JOIN OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements AS Eng
	ON Ent.EntertainerID = Eng.EntertainerID;