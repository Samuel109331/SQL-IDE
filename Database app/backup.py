def get_postegresql_attrs(table_name,host,user,password,db,port):

    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname=db,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Specify the table name
    table_name = 'your_table_name'

    # Create a cursor
    cur = conn.cursor()

    # Query to fetch column names
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"

    # Execute the query
    cur.execute(query)

    # Fetch all the results
    column_names = [row[0] for row in cur.fetchall()]

    # Close the cursor and the connection
    cur.close()
    conn.close()

    # Print the column names
    print("Column names:", column_names)