import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

countries = pd.read_csv("C:/Users/santi/OneDrive/Escritorio/Equipo - Data Rush/DataRush-RecomendacionesEstrategicas/recursos/datos/countries.csv")
holidays = pd.read_csv("C:/Users/santi/OneDrive/Escritorio/Equipo - Data Rush/DataRush-RecomendacionesEstrategicas/recursos/datos/global_holidays.csv")
passengers = pd.read_csv("C:/Users/santi/OneDrive/Escritorio/Equipo - Data Rush/DataRush-RecomendacionesEstrategicas/recursos/datos/monthly_passengers.csv")

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

#df.to_csv("resultado_limpio.csv", index=False) ---->Para pasar a csv(excel tmb pero nomas cambias la palabra)



# Total anual por país (lineas)
annual = df.groupby(['ISO3', 'Year'])['Total'].sum().reset_index()

top10 = (
    annual.groupby("ISO3")["Total"].sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

annual_top10 = annual[annual["ISO3"].isin(top10)]

plt.figure(figsize=(12,9))
sns.lineplot(data = annual_top10, x = "Year", y = "Total", hue = "ISO3", markers = "o")

plt.title("Evolución de pasajeros internacionales (Top 10 países)")
plt.xlabel("Año")
plt.ylabel("Total de pasajeros (OS)")
plt.legend(title="País (ISO3)", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()




#Promedio segun feriados (barra)
df['feriado_binario'] = df['holiday_count'].apply(lambda x: "Con feriado" if x > 0 else "Sin feriado")

avg_passengers = df.groupby('feriado_binario')['Total'].mean()
avg_passengers.plot(kind='bar', title="Promedio de pasajeros según feriados")
plt.ylabel("Promedio pasajeros (Total)")
plt.show()




#heatmap
pivot = df.pivot_table(index="Month", columns="Year", values="Total", aggfunc="mean")
#______________________________________________________________________________________________________________

# plt.figure(figsize=(12,6))
# sns.heatmap(pivot, cmap="YlGnBu", annot=False)
# plt.title("Estacionalidad de pasajeros (por mes/año)")
# plt.show()
#___________________Se veia raro, supuse que era por la diferencia en los datos________________________________

pivot_norm = pivot.div(pivot.sum(axis=0), axis=1)  # cada columna = 100%
plt.figure(figsize=(14,7))
sns.heatmap(pivot_norm, cmap="YlGnBu", annot=True, fmt=".0%")
plt.title("Meses que concentran mas viajes dentro de cada año)")
plt.show()