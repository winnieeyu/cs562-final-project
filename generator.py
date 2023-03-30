import subprocess


def main():
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """

    body = """
    for row in cur:
        if row['quant'] > 10:
            print(row)
    """

    # Note: The f allows formatting with variables.
    #       Also, note the indentation is preserved.
    tmp = f"""
import psycopg2
import psycopg2.extras

def main():
    conn = psycopg2.connect("dbname=cs562_project user=ari password=ari",
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    {body}
    
if "__main__" == __name__:
    main()
    """

    open("_generated.py", "w").write(tmp)
    subprocess.run(["python", "_generated.py"])


if "__main__" == __name__:
    main()
