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





# Total anual por país (lineas)
annual = df.groupby(['ISO3', 'Year'])['Total_OS'].sum().reset_index()

top10 = (
    annual.groupby("ISO3")["Total_OS"].sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

annual_top10 = annual[annual["ISO3"].isin(top10)]

plt.figure(figsize=(12,9))
sns.lineplot(data = annual_top10, x = "Year", y = "Total_OS", hue = "ISO3", markers = "o")

plt.title("Evolución de pasajeros internacionales (Top 10 países)")
plt.xlabel("Año")
plt.ylabel("Total de pasajeros (OS)")
plt.legend(title="País (ISO3)", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()




#Promedio segun feriados (barra)
df['feriado_binario'] = df['holiday_count'].apply(lambda x: "Con feriado" if x > 0 else "Sin feriado")

avg_passengers = df.groupby('feriado_binario')['Total_OS'].mean()
avg_passengers.plot(kind='bar', title="Promedio de pasajeros según feriados")
plt.ylabel("Promedio pasajeros (Total_OS)")
plt.show()




#heatmap
pivot = df.pivot_table(index="Month", columns="Year", values="Total_OS", aggfunc="mean")
plt.figure(figsize=(12,6))
sns.heatmap(pivot, cmap="YlGnBu", annot=False)
plt.title("Estacionalidad de pasajeros (por mes/año)")
plt.show()
