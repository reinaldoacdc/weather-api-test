import datetime
import psycopg2
import json
import os

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def list_tables():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))    
    cur = conn.cursor()

    cur.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema' ")
    row = cur.fetchall()
    print(row)

    cur.close()
    conn.commit()
    conn.close()    

def insert_historic(city, date, weekday, temp_min, temp_max):
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))    
    cur = conn.cursor()
    sql = """
        INSERT INTO public.historic(
            "CITY", "DATE", "WEEKDAY", "TEMP_MIN", "TEMP_MAX")
            VALUES (%s, %s, %s, %s, %s);
        """        
    cur.execute(sql, (city, date, weekday, temp_min, temp_max))
    cur.close()
    conn.commit()
    conn.close()    

def list_historic():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))    
    cur = conn.cursor()
    sql = """
        SELECT * FROM public.historic
        ORDER BY "ID" DESC 
        LIMIT 3;
        """        
    cur.execute(sql)

    rows = cur.fetchall()
    return(json.dumps(rows, default=default))

    cur.close()
    conn.commit()
    conn.close()    



