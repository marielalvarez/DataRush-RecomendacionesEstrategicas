from pandasql import sqldf
import pandas as pd

Holidays = pd.read_csv("C:/Users/santi/OneDrive/Escritorio/Equipo - Data Rush/DataRush-RecomendacionesEstrategicas/recursos/datos/global_holidays.csv")

query_dias_festivos_por_mes = """SELECT
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
FROM Holidays;"""
print(sqldf(query_dias_festivos_por_mes))

query_dias_festivos_por_pais = """SELECT ADM_name, 
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
FROM Holidays GROUP BY ADM_name;"""
print(sqldf(query_dias_festivos_por_pais))

query_días_festivo_por_año_por_país_divididos_en_tipo_de_día_festivo = """SELECT ADM_name AS 'Country', COUNT(DISTINCT name) FILTER (WHERE Type = 'Public holiday') AS 'Public Holidays',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Special holiday') AS 'Special holiday',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Local holiday') AS 'Local holiday',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Local observance') AS 'Local observance',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Working day (replacement)') AS 'Working day (replacement)'
FROM Holidays GROUP BY ADM_name;
"""
print(sqldf(query_días_festivo_por_año_por_país_divididos_en_tipo_de_día_festivo))

