import psycopg2
import psycopg2.extras
import tabulate


def query():
    """
    Used for testing standard queries in SQL
    """
    conn = psycopg2.connect("dbname=cs562_project user=ari password=ari",
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales WHERE quant > 10")

    return tabulate.tabulate(cur.fetchall(),
                             headers="keys", tablefmt="psql")


def main():
    print(query())


if "__main__" == __name__:
    main()
