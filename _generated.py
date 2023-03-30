
import psycopg2
import psycopg2.extras
import tabulate

def main():
    conn = psycopg2.connect("dbname=cs562_project user=ari password=ari",
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    
    _global = []
    
    for row in cur:
        if row['quant'] > 10:
            _global.append(row)
    
    
    print(tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql"))

    
if "__main__" == __name__:
    main()
    