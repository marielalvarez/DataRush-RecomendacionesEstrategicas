import csv
import sqlite3

# Input/Output files
csv_file = "C:/Users/jpfdz/Documents/GitHub/DataRush-RecomendacionesEstrategicas/recursos/datos/monthly_passengers.csv"
db_file = "datarush.db"
table_name = "Monthly_Passengers"

# Connect to (or create) database
con = sqlite3.connect(db_file)
cur = con.cursor()

# Read CSV headers
with open(csv_file, "r", newline='', encoding="utf-8") as fin:
    dr = csv.reader(fin)
    headers = next(dr)  # first row = header names
    
    # Create table dynamically
    cur.execute(f"DROP TABLE IF EXISTS {table_name};")
    cur.execute(f"CREATE TABLE {table_name} ({', '.join(headers)});")
    
    # Insert rows
    placeholders = ", ".join("?" * len(headers))
    cur.executemany(
        f"INSERT INTO {table_name} VALUES ({placeholders});",
        dr
    )

con.commit()
con.close()