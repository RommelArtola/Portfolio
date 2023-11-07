/*Sales Orders Database*/
USE SalesOrders
-- 1: Customer Liz Keyser wants to order again the products ordered on December 12, 2017. Use June 12, 2018, as the order date and June 15, 2018, as the shipped date. (1 row and 4 rows added)
--SET IDENTITY_INSERT ORDERS ON
INSERT INTO Orders (OrderNumber, OrderDate, ShipDate, CustomerID, EmployeeID)
	SELECT OrderNumber + 1000 AS NewOrderNum
		,'2018-06-12' AS OrderDate
		,'2018-06-15' AS ShipDate
		,C.CustomerID
		,EmployeeID
FROM Orders AS O
INNER JOIN Customers AS C
	ON O.CustomerID = C.CustomerID
	AND CustFirstName = 'Liz'
	AND CustLastName = 'Keyser'
	AND OrderDate = '2017-12-12' 
--SET IDENTITY_INSERT Orders OFF


INSERT INTO Order_Details (OrderNumber, ProductNumber, QuotedPrice, QuantityOrdered)
	SELECT OD.OrderNumber + 1000 AS NewOrderNum
			,ProductNumber
			,QuotedPrice
			,QuantityOrdered
	FROM Order_Details AS OD
	INNER JOIN Orders AS O
		ON O.OrderNumber = OD.OrderNumber
		AND OrderDate = '2017-12-12'
		AND CustomerID = (SELECT CustomerID 
							FROM Customers
							WHERE 0=0
							AND CustFirstName = 'Liz'
							AND CustLastName = 'Keyser'
						);







-- 2: Create a new customer record for Mary Baker at 7834 W 32nd Ct., Bothell, WA, 98011, with area code 425 and phone number 555-9876. (1 row)

INSERT INTO Customers (CustomerId,
					CustFirstName, 
						CustLastName, 
						CustStreetAddress, 
						CustCity,
						CustState,
						CustZipCode,
						CustAreaCode,
						CustPhoneNumber
						)
VALUES (1029, 'Mary', 'Baker', '7834 W 32nd Ct.', 'Bothell', 'WA', '98011', 425, '555-9876')
--It didn't let me insert without adding customerID. Did not auto calculate.



-- 3: Customer Angel Kennedy wants to order again all the products ordered during the month of November 2017. Use June 15, 2018, as the order date and June 18, 2018, as the shipped date (6, then 34).
INSERT INTO Orders (OrderNumber, OrderDate, ShipDate, CustomerID, EmployeeID)
	SELECT OrderNumber + 1000 AS NewOrderNum
		,'2018-06-15' AS OrderDate
		,'2018-06-18' AS ShipDate
		,C.CustomerID
		,EmployeeID
FROM Orders AS O
INNER JOIN Customers AS C
	ON O.CustomerID = C.CustomerID
	AND CustFirstName = 'Angel'
	AND CustLastName = 'Kennedy'
	AND MONTH(OrderDate) = 11
	AND YEAR(OrderDate) = 2017



INSERT INTO Order_Details (OrderNumber, ProductNumber, QuotedPrice, QuantityOrdered)
	SELECT OD.OrderNumber + 1000 AS NewOrderNum
			,ProductNumber
			,QuotedPrice
			,QuantityOrdered
	FROM Order_Details AS OD
	INNER JOIN Orders AS O
		ON O.OrderNumber = OD.OrderNumber
		AND MONTH(OrderDate) = 11
		AND YEAR(OrderDate) = 2017
		AND CustomerID = (SELECT CustomerID 
							FROM Customers
							WHERE 0=0
							AND CustFirstName = 'Angel'
							AND CustLastName = 'Kennedy'
						);













/*School Scheduling Database*/
USE SchoolScheduling 
-- 1: Angel Kennedy wants to register as a student. Her husband, John, is already enrolled. Create a new student record for Angel using the information from John’s record. (1 row)
INSERT INTO Students (StudentID,
						StudFirstName,
						StudLastName,
						StudStreetAddress,
						StudCity,
						StudState,
						StudZipCode,
						StudAreaCode,
						StudPhoneNumber,
						StudBirthDate,
						StudGender,
						StudMaritalStatus,
						StudMajor)
SELECT 1019 AS StudentID
		,'Angel' AS FName
		,'Kennedy' AS LName
		,StudStreetAddress
		,StudCity
		,StudState
		,StudZipCode
		,StudAreaCode
		,StudPhoneNumber
		,StudBirthDate
		,'F' AS Gender
		,StudMaritalStatus
		,StudMajor
FROM Students AS S
WHERE 0=0
AND S.StudFirstName = 'John'
AND S.StudLastName = 'Kennedy';


-- 2: Staff member Tim Smith wants to enroll as a student. Create a new student record from Tim’s staff record. (1 row)
INSERT INTO Students (StudentID,
						StudFirstName,
						StudLastName,
						StudStreetAddress,
						StudCity,
						StudState,
						StudZipCode,
						StudAreaCode,
						StudPhoneNumber,
						--StudBirthDate,
						StudGender
						--StudMaritalStatus,
						--StudMajor
						)
SELECT 1020 AS StudentID
	,StfFirstName
	,StfLastname
	,StfStreetAddress
	,StfCity
	,StfState
	,StfZipCode
	,StfAreaCode
	,StfPhoneNumber
	,'M' AS GENDER
FROM Staff
WHERE StfFirstName = 'Tim'
AND StfLastname = 'Smith'



/*Entertainment Agency Database*/
USE Entertainment
-- 1: Agent Marianne Wier would like to book some entertainers, so create a new customer record by copying relevant fields from the Agents table. (1 row)
INSERT INTO Customers (CustomerID, CustFirstName, CustLastName, CustStreetAddress, 
						CustCity, CustState, CustZipCode, CustPhoneNumber)
SELECT 10016 AS CustomerID
		,AgtFirstName, AgtLastName
		,AgtStreetAddress, AgtCity, AgtState
		,AgtZipCode, AgtPhoneNumber

FROM Agents
WHERE 0=0
AND AgtFirstName = 'Marianne'
AND AgtLastName = 'Wier'



-- 2: Add ‘New Age’ to the list of musical styles. (1 row)
INSERT INTO Musical_Styles (StyleID, StyleName)
VALUES (26, 'New Age')



-- 3: Customer Doris Hartwig would like to rebook the entertainers she hired to play on December 2, 2017, for August 1, 2018. (1 row)
INSERT INTO Engagements (EngagementNumber, StartDate, EndDate, StartTime, StopTime,
						ContractPrice, CustomerID, AgentID, EntertainerID)

SELECT 132 AS EngNum
		,'2018-08-01' AS StartDt
		,DATEADD(DAY, DATEDIFF(DAY, StartDate, EndDate), EndDate) AS NewEndDt
		,StartTime
		,StopTime
		,ContractPrice
		,CUST.CustomerID
		,AgentID
		,EntertainerID
FROM Engagements AS E
INNER JOIN (SELECT DISTINCT CustomerID
			FROM Customers
			WHERE 0=0
			AND CustFirstName = 'Doris'
			AND CustLastName = 'Hartwig'
			) AS CUST
	ON E.CustomerID = CUST.CustomerID
	AND StartDate = '2017-12-02'

