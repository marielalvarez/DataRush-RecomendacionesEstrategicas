-- Obtener el número de días festivo por año por país
SELECT ADM_name, COUNT(DISTINCT name) FROM Holidays GROUP BY ADM_name;

-- Obtener el numero de días festivos por mes
SELECT
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-01-%') AS 'January',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-02-%') AS 'Ferbruary',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-03-%') AS 'March',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-04-%') AS 'April',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-05-%') AS 'May',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-06-%') AS 'June',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-07-%') AS 'July',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-08-%') AS 'August',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-09-%') AS 'September',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-10-%') AS 'October',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-11-%') AS 'November',
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-12-%') AS 'December'
FROM Holidays;

-- Obtener el número de días festivo por mes por país
SELECT ADM_name, 
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-01-%') AS 'January',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-02-%') AS 'Ferbruary',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-03-%') AS 'March',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-04-%') AS 'April',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-05-%') AS 'May',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-06-%') AS 'June',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-07-%') AS 'July',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-08-%') AS 'August',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-09-%') AS 'September',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-10-%') AS 'October',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-11-%') AS 'November',
COUNT(DISTINCT name) FILTER (WHERE Date LIKE '%-12-%') AS 'December'
FROM Holidays GROUP BY ADM_name;

-- Obtener el número de días festivo por año por país divididos en tipo de día festivo
SELECT ADM_name AS 'Country', COUNT(DISTINCT name) FILTER (WHERE Type = 'Public holiday') AS 'Public Holidays',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Special holiday') AS 'Special holiday',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Local holiday') AS 'Local holiday',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Local observance') AS 'Local observance',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Working day (replacement)') AS 'Working day (replacement)'
FROM Holidays GROUP BY ADM_name;

-- Obtener el número de pasajeros domésticos por país
SELECT Holidays.ADM_name, SUM(Monthly_Passengers.Domestic) 
FROM Monthly_Passengers INNER JOIN Holidays ON Holidays.ISO3 = Monthly_Passengers.ISO3 
GROUP BY Holidays.ADM_name;

-- Obtener el número de pasajeros totales por país
SELECT Holidays.ADM_name, 
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) AS 'Total Passangers'
FROM Monthly_Passengers INNER JOIN Holidays ON Holidays.ISO3 = Monthly_Passengers.ISO3 
GROUP BY Holidays.ADM_name;

-- Obtener el número de pasajeros totales por país y Mes
SELECT Holidays.ADM_name, 
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '1') AS 'January Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '2') AS 'February Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '3') AS 'March Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '4') AS 'April Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '5') AS 'May Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '6') AS 'June Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '7') AS 'July Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '8') AS 'August Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '9') AS 'September Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '10') AS 'October Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '11') AS 'November Passangers',
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) 
FILTER (WHERE Monthly_Passengers.Month = '12') AS 'December Passangers'
FROM Monthly_Passengers INNER JOIN Holidays ON Holidays.ISO3 = Monthly_Passengers.ISO3 
GROUP BY Holidays.ADM_name;

-- Obtener el número total de pasajeros por

