import psycopg2
import tabulate


def main():
    """
    Used for testing standard queries in SQL
    """
    conn = psycopg2.connect("dbname=cs562_project user=ari password=ari")
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales WHERE quant > 10")

    print(tabulate.tabulate(cur.fetchall(),
                            headers=["Customer", "Product", "Quant", "Price"], tablefmt="psql"))


if "__main__" == __name__:
    main()
