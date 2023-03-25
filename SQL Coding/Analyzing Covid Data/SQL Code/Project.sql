/* Comments, Info, Intro. 
Please note this data is older than current because the source was changed. The data was extracted from the world COVID-19 dataset from link: https://ourworldindata.org/covid-deaths

Additionally, the data source was one large .CSV file and then split into two seperate .xslx files; one for COVID deaths, and the other for COVID vaccination info. 

The purpose of this project is to highlight and show some of my skills in SQL for ETL as well as visualizing this data.

*/




/* Entire Dataset for familiarity */
-- Let's first explore the data lightly by looking at location, date, case info, deaths, and population.
SELECT Location
		,Date
		,Total_Cases
		,New_Cases
		,Total_Deaths
		,Population
	FROM ProjectDB..CovidDeaths
	ORDER BY 
		Date DESC
		--total_deaths DESC





/* Tableau Visual: Total Covid Summary Table. Mortality Rate included */
-- What is the overall absolute mortality rate of COVID? Let's find out!
SELECT  
	 FORMAT(SUM(NEW_CASES), 'N') CasesTotal
	,FORMAT(SUM(CAST(NEW_DEATHS AS INT)), 'N') DeathsTotal
	,FORMAT((SUM(CAST(NEW_DEATHS AS INT))/SUM(NEW_CASES)), 'P') AS TotalMortalityRate
	,FORMAT(SUM(CAST(VAC.new_vaccinations AS BIGINT)), 'N') AS VaccinationsTotal 
	
FROM ProjectDB..CovidDeaths AS DEA
INNER JOIN ProjectDB..CovidVaccinations AS VAC
	ON DEA.LOCATION = VAC.LOCATION
	AND DEA.Date = VAC.DATE



/* Tableau Visual: COVID Infection Rate by Day and Total Cases Play Button if Available. If not, scatter plot.*/
-- Let's look at what percentage of the population of US has gotten COVID by day.

SELECT Location
	,CAST(Date AS DATE) AS DateCol
	,Population
	,Total_Cases
	,FORMAT(Total_Cases/Population, 'P') AS InfectionRate
FROM ProjectDB..CovidDeaths
WHERE Location = 'United States'
ORDER BY DateCol DESC 
--Looks like April 30th, of 2021 was the day with the highest infection rate at roughly 9.78%.




/*Tableau Visual: Play button of the data in the table (deaths, cases, mortality %) and/or bar chart/line summary of mortality by month for US. */
-- Next, let's look at the total cases vs total deaths of United States, and the respective percentage by day, too. This will be a visual on our report. For my own reference, hopefully it can be one where we can can hit play button on the Date column. Just for show, we'll make this query a temp table.
DROP TABLE IF EXISTS #MortalityOnDay
CREATE TABLE #MortalityOnDay(
	Location NVARCHAR(255),
	DateCol DATE,
	New_Cases FLOAT,
	New_Deaths FLOAT
	)

	INSERT INTO #MortalityOnDay
	SELECT LOCATION
		,Date
		,New_Cases
		,New_Deaths
	FROM ProjectDB..CovidDeaths
	WHERE 0=0
	AND Location = 'United States'
	AND Continent IS NOT NULL

SELECT Location
	,DateCol
	,SUM(New_Cases) AS NewCases
	,SUM(New_Deaths) AS NewDeaths
	,FORMAT((SUM(New_Deaths)/SUM(New_Cases)), 'P') AS MortalityRateOfInfected
FROM #MortalityOnDay
GROUP BY Location, DateCol
ORDER BY DateCol 

-- The day one was most likely to die from COVID seems to have been March  3rd, 2020 with a 9.46% likelihood.
--As an interesting note, it seems that the first recorded death was when the cases had enough traction to begin compounding more easily.






/*Tableau Visual: This table analyses the percent of population that was infected or died over the course of the time we have data for. */
-- Even though we've only looked at US-related info, I am curious to know which Location (Country) had the highest death percentage as deaths over total population as well as the infection rate of the total population.
SELECT Location
	,FORMAT(MAX(CAST(TOTAL_DEATHS AS INT)), 'N') AS TotalDeathCt
	,FORMAT(MAX(CAST(TOTAL_CASES AS INT))/MAX(POPULATION), 'P') AS PopulationPercInfected
	,FORMAT(MAX(CAST(TOTAL_DEATHS AS INT))/MAX(POPULATION), 'P') AS PopulationPercLost
FROM ProjectDB..CovidDeaths
/*We'll use having for showcasing, but the WHERE Total_Deaths is also another valid option for our intended results.
WHERE TOTAL_DEATHS IS NOT NULL */
GROUP BY Location
HAVING FORMAT(MAX(CAST(TOTAL_DEATHS AS INT)), 'N') IS NOT NULL
ORDER BY 1,2,3,4




/*Tableau Visual: Continent of Population Lost and Infected*/
-- Let's do the same, but for continets this time! This will be a visual on your dashboard/report. 
-- Creating view for visualizations later
-- DROP VIEW IF EXISTS VW_Continents_Info;

CREATE VIEW VW_Continents_Info AS
SELECT Location
	,FORMAT(MAX(CAST(TOTAL_DEATHS AS INT)), 'N') AS TotalDeathCt
	,FORMAT(MAX(CAST(TOTAL_CASES AS INT))/MAX(POPULATION), 'P') AS InfectionRate
	,FORMAT(MAX(CAST(TOTAL_DEATHS AS INT))/MAX(POPULATION), 'P') AS MortalityPercentPop
FROM ProjectDB..CovidDeaths
WHERE CONTINENT IS NULL
--Due to how the data is set up, the contients show up in the LOCATION column WHEN the continent column is Blank. Else, it shows Contient and then the country within the contient in the Location Column. Because of that, we have to specify in our clause we only want the data from the null values in the continent column.
AND LOCATION <> 'INTERNATIONAL' -- We removed international from the results because the infection and mortality rate were both null values. Also Total death was only 15. Did not seem relevant to include for the analysis I am wanting to perform/show.
GROUP BY Location

SELECT * 
FROM VW_Continents_Info
	





/*Tableau Visual (hopefully play button of what countries gets the most vaccination). If not, a static map of the countries, color coded by different things. We'll see :) */
-- Let's start with joining our tables of CovidDeaths and Vaccination Information! We'll start off by new daily data by country using a CTE.
WITH CTE_POPvsVAC (Location, Date, TotalPopulation, NewCases, NewDeaths, NewTests, NewVaccs, RunningTotalVaccsByLocation) AS(
		SELECT DEA.Location
			,DEA.Date
			,CAST(DEA.Population AS FLOAT) AS TotalPopulation
			,DEA.New_Cases
			,DEA.New_Deaths
			,VAC.New_Tests
			,VAC.New_Vaccinations
			,SUM(CONVERT(FLOAT, VAC.New_Vaccinations)) OVER(PARTITION BY DEA.Location ORDER BY DEA.LOCATION, DEA.DATE) AS RunningTotalVaccsByLocation
	
		FROM ProjectDB..CovidDeaths AS DEA
		INNER JOIN ProjectDB..CovidVaccinations AS VAC
			ON DEA.LOCATION = VAC.LOCATION 
			AND DEA.DATE = VAC.DATE
		WHERE DEA.CONTINENT IS NOT NULL

)
	SELECT Location
		,Date
		,TotalPopulation
		,NewCases
		,NewDeaths
		,NewTests
		,RunningTotalVaccsByLocation
		,FORMAT((RunningTotalVaccsByLocation/TotalPopulation), 'P') AS RunningPercentPopVaccinated
	FROM CTE_POPvsVAC

