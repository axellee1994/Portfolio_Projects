SELECT *
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
ORDER by 3,4;

--SELECT *
--FROM [Portfolio Project]..[COVID Vaccinations]
--ORDER by 3,4

--Select Data that we are going to be using
SELECT location,date,total_cases,new_cases,total_deaths,population
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
ORDER BY 1,2

-- Looking at Total Cases VS Total Deaths
-- Show likelihood of dying if you contract COVID in your country
SELECT location,date,total_cases,total_deaths, (total_deaths/total_cases)*100 AS Death_Percentage
FROM [Portfolio Project]..[COVID Deaths]
WHERE location LIKE 'Singapore' AND continent IS NOT NULL
ORDER BY 1,2;

--By continent
SELECT continent,MAX(CAST(total_deaths AS INT)) AS Total_Death_Count
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY Total_Death_Count DESC;


-- Looking at Total Cases VS Population
-- Shows what percentage of population gotten COVID 
SELECT location,date,population,total_cases,ROUND((total_cases/population)*100,3) AS Population_Infected_Percentage
FROM [Portfolio Project]..[COVID Deaths]
WHERE location LIKE 'Singapore' AND continent IS NOT NULL
ORDER BY 1,2;

-- Looking at countries with highest infection rate VS population
SELECT location,population,MAX(total_cases) AS Highest_Infection_Count, ROUND(MAX(total_cases/population)*100,3) AS Population_Infected_Percentage
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
GROUP BY location,population
ORDER BY Population_Infected_Percentage DESC;

-- Showing countries with highest death count per population
SELECT location,MAX(CAST(total_deaths AS INT)) AS Total_Death_Count
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY Total_Death_Count DESC;

-- Showing continents with the highest death count per population
SELECT continent,MAX(CAST(total_deaths AS INT)) AS Total_Death_Count
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY Total_Death_Count DESC;

-- Global Numbers 
SELECT SUM(new_cases) AS Total_Cases, SUM(CAST(new_deaths AS INT)) AS Total_Deaths, (SUM(CAST(new_deaths AS INT))/SUM(new_cases))*100 AS Death_Percentage
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
ORDER BY 1,2;

-- Global Numbers by date
SELECT date,SUM(new_cases) AS Total_Cases, SUM(CAST(new_deaths AS INT)) AS Total_Deaths, (SUM(CAST(new_deaths AS INT))/SUM(new_cases))*100 AS Death_Percentage
FROM [Portfolio Project]..[COVID Deaths]
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1,2;

-- Looking at Total Populations VS Vaccinations
SELECT dea.continent,dea.location,dea.date, dea.population,vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.location ORDER BY dea.location,dea.date) AS Rolling_Cummulative_Vaccinations
FROM [Portfolio Project]..[COVID Deaths] dea
JOIN [Portfolio Project]..[COVID Vaccinations] vac
  ON  dea.location = vac.location
  AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2,3;

--OPTION 1: CTE
WITH PopvsVac (Continent, location, date, population,New_Vaccinations,Rolling_Cummulative_Vaccinations)
AS(
SELECT dea.continent,dea.location,dea.date, dea.population,vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.location ORDER BY dea.location,dea.date) AS Rolling_Cummulative_Vaccinations
FROM [Portfolio Project]..[COVID Deaths] dea
JOIN [Portfolio Project]..[COVID Vaccinations] vac
  ON  dea.location = vac.location
  AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
)
SELECT *, (Rolling_Cummulative_Vaccinations / population) * 100 AS Rolling_Vaccination_Percentage
FROM PopvsVac;

--OPTION 2: TEMP TABLE
DROP TABLE IF exists #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar (255),
Date datetime,
Population numeric,
New_vaccinations numeric,
Rolling_Cummulative_Vaccinations numeric
)
INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent,dea.location,dea.date, dea.population,vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.location ORDER BY dea.location,dea.date) AS Rolling_Cummulative_Vaccinations
FROM [Portfolio Project]..[COVID Deaths] dea
JOIN [Portfolio Project]..[COVID Vaccinations] vac
  ON  dea.location = vac.location
  AND dea.date = vac.date
WHERE dea.continent IS NOT NULL

SELECT *, (Rolling_Cummulative_Vaccinations / population) * 100 AS Rolling_Vaccination_Percentage
FROM #PercentPopulationVaccinated

--Creating View to store data for later visualizations
CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent,dea.location,dea.date, dea.population,vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.location ORDER BY dea.location,dea.date) AS Rolling_Cummulative_Vaccinations
FROM [Portfolio Project]..[COVID Deaths] dea
JOIN [Portfolio Project]..[COVID Vaccinations] vac
  ON  dea.location = vac.location
  AND dea.date = vac.date
WHERE dea.continent IS NOT NULL;

SELECT *
FROM PercentPopulationVaccinated