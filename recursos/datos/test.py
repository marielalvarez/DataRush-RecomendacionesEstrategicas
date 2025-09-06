import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandasql import sqldf

countries = pd.read_csv("C:/Users/jpfdz/Documents/GitHub/DataRush-RecomendacionesEstrategicas/recursos/datos/countries.csv")
holidays = pd.read_csv("C:/Users/jpfdz/Documents/GitHub/DataRush-RecomendacionesEstrategicas/recursos/datos/global_holidays.csv")
passengers = pd.read_csv("C:/Users/jpfdz/Documents/GitHub/DataRush-RecomendacionesEstrategicas/recursos/datos/monthly_passengers.csv")

#fechas
holidays['Date'] = pd.to_datetime(holidays['Date'])
holidays['Year'] = holidays['Date'].dt.year
holidays['Month'] = holidays['Date'].dt.month

#fechas mensuales con pasajeros
passengers['date'] = pd.to_datetime(
    passengers['Year'].astype(str) + "-" + passengers['Month'].astype(str) + "-01"
)

#contar feriados
holidays_monthly = (
    holidays.groupby(['ISO3', 'Year', 'Month'])
    .size()
    .reset_index(name='holiday_count')
)

#unir a pasajeros
df = passengers.merge(
    holidays_monthly,
    on=['ISO3', 'Year', 'Month'],
    how='left'
)

# Donde no hay feriados → 0
df['holiday_count'] = df['holiday_count'].fillna(0)

#Dataset final, imprimie las 1eras 13 lineas
print(df.head(13))
print(df.info())

# Obtener el numero de días festivos por mes
festDayQuery = """
SELECT
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-01-%') AS January,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-02-%') AS February,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-03-%') AS March,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-04-%') AS April,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-05-%') AS May,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-06-%') AS June,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-07-%') AS July,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-08-%') AS August,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-09-%') AS September,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-10-%') AS October,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-11-%') AS November,
SUM(DISTINCT name) FILTER (WHERE Date LIKE '%-12-%') AS December
FROM holidays
"""
festDayResult = sqldf(festDayQuery, locals())
festDay_months = festDayResult.T.reset_index()
festDay_months.columns = ["Month", "Holiday_Count"]

plt.figure(figsize=(12,6))
sns.barplot(data=festDay_months, x="Month", y="Holiday_Count", palette="viridis")
plt.title("Número de días festivos por mes")
plt.xticks(rotation=45)
plt.ylabel("Contado de días festivos")
plt.show()

# Obtener el número de días festivo por mes por país
festDayMonthQuery = """
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
FROM holidays GROUP BY ADM_name;
"""

""" festDayMonthResult = sqldf(festDayMonthQuery, locals())

festDayMonthResultMelted = festDayMonthResult.melt(
    id_vars="ADM_name",
    var_name="Month",
    value_name="Holiday_Count"
)

plt.figure(figsize=(14,7))
sns.barplot(
    data=festDayMonthResultMelted,
    x="Month", 
    y="Holiday_Count", 
    hue="ADM_name"
)
plt.xticks(rotation=45)
plt.title("Distinct Holidays per Month by Country")
plt.ylabel("Number of Distinct Holidays")
plt.show() """

# Obtener el número de pasajeros totales por país
passangerCountriesQuery = """
SELECT holidays.ADM_name, 
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) AS 'Total_Passengers'
FROM passengers INNER JOIN holidays ON holidays.ISO3 = passengers.ISO3 
GROUP BY holidays.ADM_name;
"""
passangerCountriesResult = sqldf(passangerCountriesQuery, locals())

plt.figure(figsize=(12,6))
sns.barplot(data=passangerCountriesResult, x='ADM_name', y='Total_Passengers')
plt.xticks(rotation=90)  # Rotate country names for readability
plt.title('Pasajeros Totales por País')
plt.ylabel('Pasajeros totales')
plt.xlabel('Country')
plt.tight_layout()
plt.show()