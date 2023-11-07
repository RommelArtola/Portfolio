/*Sales Orders Database*/
--1: Show me all the information on our employees.
SELECT * 
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Employees AS EMP;


--2: Show me a list of cities, in alphabetical order, where our vendors are located, and include the names of the vendors we work with in each city.
SELECT	VendCity AS Vendor_City
		,VendName AS Vendor_Name
FROM OMSBA23_ARTOLA_SalesOrdersExample.dbo.Vendors
ORDER BY Vendor_City DESC;



/*Entertainment Agency Database*/
--1: Give me the names and phone numbers of all our agents, and list them in last name/first name order.
SELECT AgtLastName
		,AgtCity
		,AgtPhoneNumber
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Agents;


--2: Give me the information on all our engagements.
SELECT *
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements;


--3: List all engagements and their associated start dates. Sort the records by date in descending order and by engagement in ascending order.
SELECT EngagementNumber
	,StartDate
FROM OMSBA23_ARTOLA_EntertainmentAgencyExample.dbo.Engagements
ORDER BY StartDate DESC, EngagementNumber ASC;




/*School Scheduling Database*/
--1: Show me a complete list of all the subjects we offer.
SELECT SubjectName
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Subjects;


--2: What kinds of titles are associated with our faculty?
SELECT DISTINCT Title
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Faculty;


--3: List the names and phone numbers of all our staff, and sort them by last name and first name.
SELECT StfLastName
		,StfFirstName
		,StfPhoneNumber
FROM OMSBA23_ARTOLA_SchoolSchedulingExample.dbo.Staff
ORDER BY StfLastName, StfFirstName;



/*Bowling League Database*/
--1: List all of the teams in alphabetical order.
SELECT TeamName
FROM OMSBA23_ARTOLA_BowlingLeagueExample.dbo.Teams
ORDER BY TeamName;

--2: Show me all the bowling score information for each of our members.
SELECT *
FROM OMSBA23_ARTOLA_BowlingLeagueExample.dbo.Bowler_Scores;

--3: Show me a list of bowlers and their addresses, and sort it in alphabetical order.
SELECT CONCAT(BowlerLastName, ', ', BowlerFirstName) AS BowlerFullName
		,BowlerAddress
FROM OMSBA23_ARTOLA_BowlingLeagueExample.dbo.Bowlers
ORDER BY BowlerLastName, BowlerFirstName;


/*Recipes Database*/
--1: Show me a list of all the ingredients we currently keep track of
SELECT *
FROM OMSBA23_ARTOLA_RecipesExample.dbo.Ingredients;

--2: Show me all the main recipe information, and sort it by the name of the recipe in alphabetical order.
SELECT *
FROM OMSBA23_ARTOLA_RecipesExample.dbo.Recipes
ORDER BY RecipeTitle;