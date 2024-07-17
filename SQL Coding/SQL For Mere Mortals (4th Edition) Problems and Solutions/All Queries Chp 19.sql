














/*Sales Orders Database*/
-- 1: Show all customers and display whether they placed an order in the first week of December 2017. (28 rows)
USE SalesOrders
SELECT C.CustomerID
		,CustLastName + ', ' + CustFirstName AS CustName
		,OrderPlacedFirstWeekDec2017
FROM Customers AS C
LEFT JOIN (SELECT CustomerID
					,MAX(CASE
					WHEN OrderDate 
						BETWEEN CAST('2017-12-01' AS DATE) 
						AND CAST('2017-12-07' AS DATE) THEN 1
					ELSE 0
					END
					) AS OrderPlacedFirstWeekDec2017
			FROM Orders 
			GROUP BY CustomerID
			) AS O
	ON C.CustomerID = O.CustomerID
ORDER BY C.CustomerID;


-- 2: List customers and the state they live in spelled out. (28 rows)
SELECT CustLastName + ', ' + CustFirstName  AS CustName
		,CASE  
			WHEN CustState = 'CA' THEN 'California'
			WHEN CustState = 'OR' THEN 'Oregon'
			WHEN CustState = 'TX' THEN 'Texas'
			WHEN CustState = 'WA' THEN 'Washington'
			END AS CustFullState

FROM Customers AS C



-- 3: Display employees and their age as of February 15, 2018. (8 rows)
SELECT EmpLastName + ', ' + EmpFirstName AS EmpName
		,EmpBirthDate
		
		,DATEDIFF(YEAR, EmpBirthDate, '2018-02-15') AS EMP_AGE 
		--As of Feb 15, 2018..
FROM Employees AS E





/*School Scheduling Database*/
USE SchoolScheduling
-- 1: Display student Marital Status based on a code. (18 rows)
SELECT StudentID
		,StudLastName + ', ' + StudFirstName AS StudName
		,CASE 
			WHEN StudMaritalStatus = 'S' THEN 'Single'
			WHEN StudMaritalStatus = 'W' THEN 'Widows'
			WHEN StudMaritalStatus = 'D' THEN 'Divorced'
			WHEN StudMaritalStatus = 'M' THEN 'Married'
			ELSE 'Unassigned/Null'
			END AS StudMaritalStatus_DESC
FROM Students



--2: Calculate student age as of November 15, 2017. (18 rows)
SELECT StudLastName + ', ' + StudFirstName AS StudName
		,DATEDIFF(YEAR, StudBirthDate, '2017-09-15') AS STUD_AGE
		--As of November 15, 2017
FROM Students AS E






/*Entertainment Agency Database*/
USE Entertainment
-- 1: Display Customers and their preferred styles, but change 50’s, 60’s, 70’s, and 80’s music to ‘Oldies’. (36 rows)
SELECT CustLastName + ', ' + CustFirstName AS CustName
		,NewStyleName
FROM Customers AS C
LEFT JOIN Musical_Preferences AS MP
	ON C.CustomerID = MP.CustomerID
LEFT JOIN (SELECT StyleID
				  ,StyleName
				  ,CASE WHEN
							StyleName LIKE ('%50%') OR
							StyleName LIKE ('%60%') OR
							StyleName LIKE ('%70%') OR
							StyleName LIKE ('%80%')
						THEN 'Oldies'
					ELSE StyleName --Could also bucket a 'Other' instead.
					END AS NewStyleName
			FROM Musical_Styles AS MS
			) AS MS
	ON MP.StyleID = MS.StyleID;




-- 2: Find Entertainers who play Jazz but not Contemporary musical styles. (1 row)
SELECT E.EntertainerID
	   ,E.EntStageName
	   ,PLAYS_JAZZ
	   ,PLAYS_CONTEMP
FROM Entertainers AS E

INNER JOIN (SELECT DISTINCT EntertainerID
					,CASE WHEN StyleName = 'Jazz' THEN 1 ELSE 0 END AS PLAYS_JAZZ
			FROM Entertainer_Styles AS ES
			INNER JOIN Musical_Styles AS MS
				ON ES.StyleID = MS.StyleID
			WHERE StyleName = 'JAZZ') AS JAZZ
	ON E.EntertainerID = JAZZ.EntertainerID

LEFT JOIN (SELECT DISTINCT EntertainerID
					,CASE WHEN StyleName = 'Contemporary' THEN 1 ELSE 0 END AS PLAYS_CONTEMP
			FROM Entertainer_Styles AS ES
			INNER JOIN Musical_Styles AS MS
				ON ES.StyleID = MS.StyleID
			WHERE StyleName = 'CONTEMPORARY') AS CONTEMP
	ON E.EntertainerID = CONTEMP.EntertainerID

WHERE 0=0
AND PLAYS_JAZZ = 1
AND COALESCE(PLAYS_CONTEMP, 0) = 0;