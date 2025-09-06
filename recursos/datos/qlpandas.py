from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

Holidays = pd.read_csv("C:/Users/santi/OneDrive/Escritorio/Equipo - Data Rush/DataRush-RecomendacionesEstrategicas/recursos/datos/global_holidays.csv")
Monthly_Passengers = pd.read_csv("C:/Users/santi/OneDrive/Escritorio/Equipo - Data Rush/DataRush-RecomendacionesEstrategicas/recursos/datos/monthly_passengers.csv")








df_dias_festivos_por_mes = sqldf("""SELECT
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
FROM Holidays;""")

# Preparar los datos
data_transposed = df_dias_festivos_por_mes.T  # Transponer
data_transposed.columns = ['Holidays_Count']  # Renombrar columna
data_transposed.index.name = 'Month'

# Crear el gráfico de barras
plt.figure(figsize=(12, 6))
plt.bar(data_transposed.index, data_transposed['Holidays_Count'], color='skyblue', edgecolor='navy')
plt.title('Días Festivos por Mes', fontsize=16, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Número de Días Festivos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()









df_dias_festivos_por_pais = sqldf("""SELECT ADM_name, 
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
FROM Holidays GROUP BY ADM_name;""")
print(df_dias_festivos_por_pais)

# Calcular totales
df_total = df_dias_festivos_por_pais.copy()
months_cols = [col for col in df_total.columns if col != 'ADM_name']
df_total['Total'] = df_total[months_cols].sum(axis=1)

# Top 10 altos y bajos
top_10_altos = df_total.nlargest(10, 'Total')['ADM_name'].tolist()
top_10_bajos = df_total.nsmallest(10, 'Total')['ADM_name'].tolist()

# Filtrar DataFrame original
selected_countries = top_10_altos + top_10_bajos
df_filtered = df_dias_festivos_por_pais[df_dias_festivos_por_pais['ADM_name'].isin(selected_countries)]

# Preparar para heatmap
df_heatmap = df_filtered.set_index('ADM_name')

plt.figure(figsize=(12, 10))
sns.heatmap(df_heatmap, 
            annot=True,
            fmt='d',
            cmap='RdYlBu_r',
            cbar_kws={'label': 'Días Festivos'})

plt.title('Días Festivos por Mes - Top 10 MÁS Altos y MÁS Bajos', fontsize=16, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('País', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()






df_días_festivo_por_año_por_país_divididos_en_tipo_de_día_festivo = sqldf("""SELECT ADM_name AS 'Country', COUNT(DISTINCT name) FILTER (WHERE Type = 'Public holiday') AS 'Public Holidays',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Special holiday') AS 'Special holiday',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Local holiday') AS 'Local holiday',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Local observance') AS 'Local observance',
COUNT(DISTINCT name) FILTER (WHERE Type = 'Working day (replacement)') AS 'Working day (replacement)'
FROM Holidays GROUP BY ADM_name;
""")
print(df_días_festivo_por_año_por_país_divididos_en_tipo_de_día_festivo)

import matplotlib.pyplot as plt

# Calcular total de días festivos por país para ordenar
df_plot = df_días_festivo_por_año_por_país_divididos_en_tipo_de_día_festivo.copy()
type_columns = ['Public Holidays', 'Special holiday', 'Local holiday', 'Local observance', 'Working day (replacement)']
df_plot['Total'] = df_plot[type_columns].sum(axis=1)

# Top 15 países con más días festivos
top_15 = df_plot.nlargest(15, 'Total')

# Crear gráfico de barras apiladas
plt.figure(figsize=(15, 8))
bottom = [0] * len(top_15)

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
for i, col in enumerate(type_columns):
    plt.bar(top_15['Country'], top_15[col], bottom=bottom, 
            label=col, color=colors[i], alpha=0.8)
    bottom = [bottom[j] + top_15[col].iloc[j] for j in range(len(top_15))]

plt.title('Tipos de Días Festivos por País (Top 15)', fontsize=16, fontweight='bold')
plt.xlabel('País', fontsize=12)
plt.ylabel('Número de Días Festivos', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()








df_pasajeros_domesticos_por_pais = sqldf("""SELECT Holidays.ADM_name, SUM(Monthly_Passengers.Domestic) 
FROM Monthly_Passengers INNER JOIN Holidays ON Holidays.ISO3 = Monthly_Passengers.ISO3 
GROUP BY Holidays.ADM_name;""")
print(df_pasajeros_domesticos_por_pais)

import matplotlib.pyplot as plt

df_pasajeros_domesticos_por_pais.columns = ['Country', 'Domestic_Passengers']

# Top 10 y Bottom 10
top_10_domesticos = df_pasajeros_domesticos_por_pais.nlargest(10, 'Domestic_Passengers')
bottom_10_domesticos = df_pasajeros_domesticos_por_pais.nsmallest(10, 'Domestic_Passengers')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Top 10
bars1 = ax1.barh(top_10_domesticos['Country'], top_10_domesticos['Domestic_Passengers'], color='darkred', alpha=0.7)
ax1.set_title('Top 10 Países con MÁS Pasajeros Domésticos', fontsize=14, fontweight='bold')
ax1.set_xlabel('Pasajeros Domésticos', fontsize=12)
ax1.invert_yaxis()
ax1.grid(axis='x', alpha=0.3)

# Añadir valores
for bar in bars1:
    width = bar.get_width()
    ax1.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
f'{width:,.0f}', ha='left', va='center', fontsize=9)

# Bottom 10
bars2 = ax2.barh(bottom_10_domesticos['Country'], bottom_10_domesticos['Domestic_Passengers'], color='darkblue', alpha=0.7)
ax2.set_title('Top 10 Países con MENOS Pasajeros Domésticos', fontsize=14, fontweight='bold')
ax2.set_xlabel('Pasajeros Domésticos', fontsize=12)
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

# Añadir valores
for bar in bars2:
    width = bar.get_width()
    ax2.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
f'{width:,.0f}', ha='left', va='center', fontsize=9)

plt.tight_layout()
plt.show()













df_pasajeros_totales_por_pais = sqldf("""SELECT Holidays.ADM_name, 
SUM(CASE WHEN Monthly_Passengers.Total IS NOT NULL THEN Monthly_Passengers.Total_OS ELSE Monthly_Passengers.Total END) AS 'Total Passangers'
FROM Monthly_Passengers INNER JOIN Holidays ON Holidays.ISO3 = Monthly_Passengers.ISO3 
GROUP BY Holidays.ADM_name;""")

print(df_pasajeros_totales_por_pais)

import matplotlib.pyplot as plt

df_pasajeros_totales_por_pais.columns = ['Country', 'Total_Passengers']
top_20_totales = df_pasajeros_totales_por_pais.nlargest(20, 'Total_Passengers')

plt.figure(figsize=(14, 12))
bars = plt.barh(top_20_totales['Country'], top_20_totales['Total_Passengers'], 
                color='darkorange', alpha=0.8)

plt.title('Top 20 Países con Más Pasajeros Totales', fontsize=16, fontweight='bold')
plt.xlabel('Número Total de Pasajeros', fontsize=12)
plt.ylabel('País', fontsize=12)

# Añadir valores en las barras
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
f'{width:,.0f}', ha='left', va='center', fontsize=10)

plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.ticklabel_format(style='plain', axis='x')
plt.tight_layout()
plt.show()






df_número_de_días_festivo_por_mes_por_país = sqldf("""
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
""")

import seaborn as sns
import matplotlib.pyplot as plt

# Preparar datos
df_heatmap = df_número_de_días_festivo_por_mes_por_país.set_index('ADM_name')

# Filtrar solo países con datos significativos (más de 5 días festivos totales)
months_cols = ['January', 'Ferbruary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df_heatmap['Total'] = df_heatmap[months_cols].sum(axis=1)
df_filtered = df_heatmap[df_heatmap['Total'] > 5].drop('Total', axis=1)

# Crear heatmap
plt.figure(figsize=(14, 16))
sns.heatmap(df_filtered, 
            annot=True, 
            fmt='d', 
            cmap='YlOrRd',
            cbar_kws={'label': 'Número de Días Festivos'},
            linewidths=0.5)

plt.title('Días Festivos por Mes y País', fontsize=16, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('País', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()












df_número_de_pasajeros_totales_por_país_y_Mes = sqldf("""
SELECT Holidays.ADM_name, 
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '1') AS 'January Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '2') AS 'February Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '3') AS 'March Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '4') AS 'April Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '5') AS 'May Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '6') AS 'June Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '7') AS 'July Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '8') AS 'August Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '9') AS 'September Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '10') AS 'October Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '11') AS 'November Passengers',
SUM(CASE WHEN passengers.Total IS NOT NULL THEN passengers.Total_OS ELSE passengers.Total END) 
FILTER (WHERE passengers.Month = '12') AS 'December Passengers'
FROM passengers INNER JOIN holidays ON holidays.ISO3 = passengers.ISO3 
GROUP BY Holidays.ADM_name;
""")
print(df_número_de_pasajeros_totales_por_país_y_Mes)

