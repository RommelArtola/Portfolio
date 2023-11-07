/*Sales Orders Database*/
USE SalesOrders
-- 1: Delete products that have never been ordered. (4 rows, then 2)
DELETE FROM Product_Vendors
WHERE ProductNumber IN (SELECT PV.ProductNumber
						FROM Product_Vendors AS PV
						FULL JOIN Order_Details AS OD
							ON PV.ProductNumber = OD.ProductNumber
						WHERE OD.ProductNumber IS NULL
					)

DELETE FROM Products
WHERE NOT EXISTS (SELECT 1
					FROM Product_Vendors AS PV
					WHERE Products.ProductNumber = PV.ProductNumber
					)


-- 2: Delete employees who haven’t sold anything. (1 or 2)
DELETE FROM Employees
WHERE EmployeeID NOT IN (SELECT EmployeeID
                          FROM Orders)
--The query is correct... but I don't have any records of employees not selling anything..
--Double and triple checked individually on source tables.



-- 3: Delete any categories that have no products. (1)
DELETE FROM Categories
WHERE CategoryID NOT IN (SELECT CategoryID
						FROM Products)
--Again.. correct query for sure, no products missing category. Checked source tables, too.




/*School Scheduling Database*/
USE SchoolScheduling 
-- 1: Delete all students who are not registered for any class.(1 or 2)
DELETE FROM Students
WHERE StudentID NOT IN (SELECT StudentID FROM Student_Schedules)



-- 2: Delete subjects that have no classes. (I got 20, then 10)
--First
DELETE FROM Faculty_Subjects
WHERE SubjectID NOT IN (SELECT SubjectID
                        FROM Classes)
--Second
DELETE FROM Subjects
WHERE SubjectID NOT IN (SELECT SubjectID
                        FROM Classes);




/*Entertainment Agency Database*/
USE Entertainment
-- 1: Delete customers who have never booked an entertainer. (5, then 2 or 3)
--First
DELETE FROM Musical_Preferences
WHERE CustomerID NOT IN (SELECT CustomerID FROM Engagements)

--Second
DELETE FROM Customers
WHERE CustomerID NOT IN (SELECT CustomerID FROM Engagements)



-- 2: Delete musical styles that aren’t played by any entertainer. (I got 6. We had 5 + we added 1 in previous chapter, not 3.)
DELETE FROM Musical_Styles
WHERE StyleID NOT IN (SELECT StyleID 
					FROM Musical_Preferences
					UNION
					SELECT StyleID
					FROM Entertainer_Styles)



-- 3: Delete members who are not part of an entertainment group. (0 rows)
DELETE FROM Members
WHERE MemberID NOT IN (SELECT MemberID FROM Entertainer_Members)