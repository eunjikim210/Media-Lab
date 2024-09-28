import sqlite3
import pandas as pd
import re

db_paths = [
    "nela-gt-2022.db",
    "nela-gt-2021.db",
    "nela-gt-2020.db",
    "nela-gt-2019.db"
]


excel_path = r"newsmax_19_22.xlsx"

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    for db_path in db_paths:

        # year = db_path.split('/')[-2].split('-')[-1]
        year_match = re.search(r'(\d{4})', db_path)
        if year_match:
            year = year_match.group(1)
        else:
            print(f"Could not extract year from path: {db_path}")
            continue
        

        conn = sqlite3.connect(db_path)
        
        query = "SELECT * FROM newsdata WHERE source = 'newsmax'"
        df = pd.read_sql(query, conn)
        
        df.to_excel(writer, sheet_name=year, index=False)
        
        conn.close()

print(f"Data saved to {excel_path}")