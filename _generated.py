
import psycopg2
import psycopg2.extras

def main():
    conn = psycopg2.connect("dbname=cs562_project user=ari password=ari",
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    
    for row in cur:
        if row['quant'] > 10:
            print(row)
    
    
if "__main__" == __name__:
    main()
    