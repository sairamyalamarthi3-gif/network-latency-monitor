import pandas as pd
import sqlite3

def save_to_csv(df, filename="history.csv"):
    df.to_csv(filename, index=False)


def save_to_sqlite(df, db="history.db"):
    conn = sqlite3.connect(db)
    df.to_sql("network_history", conn, if_exists="append", index=False)
    conn.close()
