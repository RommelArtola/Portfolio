/*Sales Orders Database*/
--1: Give me the names of all vendors based in Ballard, Bellevue, and Redmond.			(3)
SELECT VendName
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Vendors
WHERE VendCity IN ('Ballard','Bellevue', 'Redmond');


--2: Show me an alphabetized list of products with a retail price of $125.00 or more.	(13)
SELECT ProductName
		,RetailPrice
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Products
WHERE RetailPrice >= 125
ORDER BY 1;

--3: Which vendors do we work with that don’t have a Web site?							(4)
SELECT VendName
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Vendors
WHERE VendWebPage IS NULL;








/*School Scheduling Database*/
--1: Show me which staff members use a post office box as their address. (3)
SELECT CONCAT(StfLastName, ', ', StfFirstName) AS StfName
		,StfStreetAddress
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff
WHERE UPPER(StfStreetAddress) LIKE '%BOX%';



--2: Can you show me which students live outside of the Pacific Northwest? (5)
SELECT * 
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Students
WHERE StudState NOT IN ('OR', 'WA');



--3: List all the subjects that have a subject code starting ‘MUS’		(4)
SELECT *
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Subjects
WHERE SubjectCode LIKE 'MUS%';

--4: Produce a list of the ID numbers all the Associate Professors who are employed full time (4)
SELECT StaffID
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Faculty
WHERE 0=0
AND Title = 'Associate Professor'
AND Status = 'Full Time'
AND Tenured = 1;


/*Entertainment Agency Database*/
--MISSING
--1: Let me see a list of all engagements that occurred during October 2017. (24)
SELECT EngagementNumber
		,StartDate
		,EndDate
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements
WHERE 0=0
AND (StartDate BETWEEN '2017-10-01' AND '2017-10-31'
OR EndDate BETWEEN '2017-10-01' AND '2017-10-31')


--2: Show me any engagements in October 2017 that start between noon and 5 p.m. (17)
SELECT EngagementNumber
		,StartDate
		,EndDate
		,StartTime
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements
WHERE 0=0
AND (StartDate BETWEEN '2017-10-01' AND '2017-10-31'
OR EndDate BETWEEN '2017-10-01' AND '2017-10-31')
AND StartTime BETWEEN '12:00:00' and '17:00:00';


--3: List all the engagements that start and end on the same day. (5)
SELECT EngagementNumber
		,StartDate
		,EndDate
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements
WHERE StartDate = EndDate;